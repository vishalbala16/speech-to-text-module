import threading
import time
import numpy as np
import sounddevice as sd
from deepgram import DeepgramClient, PrerecordedOptions
import io
import wave
from config import DEEPGRAM_API_KEY, WAKE_WORD, SLEEP_WORD, SAMPLE_RATE, CHANNELS, CHUNK_DURATION

class SpeechToTextModule:
    def __init__(self, wake_word=None, sleep_word=None, api_key=None):
        self.wake_word = (wake_word or WAKE_WORD).lower()
        self.sleep_word = (sleep_word or SLEEP_WORD).lower()
        
        self.api_key = api_key or DEEPGRAM_API_KEY
        self.deepgram = DeepgramClient(self.api_key)
        
        self.is_listening = False
        self.is_awake = False  # TRUE WAKE/SLEEP STATE
        self.audio_thread = None
        self.transcription_callback = None
        
        # Audio settings
        self.channels = CHANNELS
        self.rate = SAMPLE_RATE
        self.record_seconds = CHUNK_DURATION
        
        # Cost tracking
        self.api_calls_count = 0
        
    def set_transcription_callback(self, callback):
        """Set callback function to handle transcription results"""
        self.transcription_callback = callback
        
    def start_listening(self):
        """Start listening for wake word only"""
        if self.is_listening:
            return
            
        self.is_listening = True
        self.is_awake = False  # Start in sleep mode
        self.audio_thread = threading.Thread(target=self._listen_continuously)
        self.audio_thread.daemon = True
        self.audio_thread.start()
        print(f"Started listening for wake word '{self.wake_word}'...")
        
    def stop_listening(self):
        """Stop the listening process"""
        self.is_listening = False
        self.is_awake = False
        if self.audio_thread:
            self.audio_thread.join()
        print(f"Stopped listening. Total API calls: {self.api_calls_count}")
        
    def _listen_continuously(self):
        """Main listening loop"""
        try:
            while self.is_listening:
                audio_data = sd.rec(
                    int(self.record_seconds * self.rate),
                    samplerate=self.rate,
                    channels=self.channels,
                    dtype=np.float32
                )
                sd.wait()
                
                if not self.is_listening:
                    break
                    
                # CORRECT LOGIC: Only process based on wake/sleep state
                self._process_audio_correctly(audio_data)
                
        except Exception as e:
            print(f"Error in listening loop: {e}")
            
    def _process_audio_correctly(self, audio_data):
        """
        CORRECT IMPLEMENTATION:
        - Sleep mode: Only check for wake word (minimal processing)
        - Awake mode: Full transcription until sleep word
        """
        try:
            # Skip if silence
            if np.max(np.abs(audio_data)) < 0.005:
                return
            
            # SLEEP MODE: Only listen for wake word
            if not self.is_awake:
                # Use simple local detection to avoid unnecessary API calls
                if self._has_potential_speech(audio_data):
                    text = self._transcribe_audio(audio_data)
                    if text and self.wake_word in text.lower():
                        self.is_awake = True
                        print(f"\n[WAKE] WAKE WORD '{self.wake_word}' DETECTED! Module is now AWAKE")
                        if self.transcription_callback:
                            self.transcription_callback(f"[WAKE] Module activated - say '{self.sleep_word}' to deactivate")
            
            # AWAKE MODE: Full transcription
            else:
                text = self._transcribe_audio(audio_data)
                if not text:
                    return
                
                # Check for sleep word first
                if self.sleep_word in text.lower():
                    self.is_awake = False
                    print(f"[SLEEP] SLEEP WORD '{self.sleep_word}' DETECTED! Module is now SLEEPING")
                    if self.transcription_callback:
                        self.transcription_callback(f"[SLEEP] Module deactivated - say '{self.wake_word}' to activate")
                else:
                    # Send transcription only when awake
                    if self.transcription_callback:
                        self.transcription_callback(text)
                        
        except Exception as e:
            print(f"Error processing audio: {e}")
    
    def _has_potential_speech(self, audio_data):
        """Simple local speech detection to minimize API calls"""
        energy = np.mean(np.abs(audio_data))
        return energy > 0.01
    
    def _transcribe_audio(self, audio_data):
        """Transcribe audio using Deepgram API"""
        try:
            # Convert to WAV
            wav_buffer = io.BytesIO()
            with wave.open(wav_buffer, 'wb') as wav_file:
                wav_file.setnchannels(self.channels)
                wav_file.setsampwidth(2)
                wav_file.setframerate(self.rate)
                audio_int16 = (audio_data * 32767).astype(np.int16)
                wav_file.writeframes(audio_int16.tobytes())
            
            wav_buffer.seek(0)
            
            # API call tracking
            self.api_calls_count += 1
            mode = "AWAKE" if self.is_awake else "SLEEP"
            print(f"API Call #{self.api_calls_count} ({mode} mode)")
            
            # Deepgram transcription
            payload = {"buffer": wav_buffer.read()}
            options = PrerecordedOptions(model="nova-2", smart_format=True)
            response = self.deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)
            
            if response.results and response.results.channels:
                alternatives = response.results.channels[0].alternatives
                if alternatives:
                    return alternatives[0].transcript.strip()
            
            return ""
            
        except Exception as e:
            print(f"Error in transcription: {e}")
            return ""
    
    def get_status(self):
        """Get current module status"""
        return "AWAKE" if self.is_awake else "SLEEPING"
    
    def __del__(self):
        """Cleanup"""
        self.stop_listening()