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
        self.is_transcribing = False
        self.audio_thread = None
        self.transcription_callback = None
        
        # Audio settings
        self.channels = CHANNELS
        self.rate = SAMPLE_RATE
        self.record_seconds = CHUNK_DURATION
        
    def set_transcription_callback(self, callback):
        """Set callback function to handle transcription results"""
        self.transcription_callback = callback
        
    def start_listening(self):
        """Start the continuous listening process"""
        if self.is_listening:
            return
            
        self.is_listening = True
        self.audio_thread = threading.Thread(target=self._listen_continuously)
        self.audio_thread.daemon = True
        self.audio_thread.start()
        print("Started listening for wake word...")
        
    def stop_listening(self):
        """Stop the listening process"""
        self.is_listening = False
        self.is_transcribing = False
        if self.audio_thread:
            self.audio_thread.join()
        print("Stopped listening")
        
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
                    
                # Process the audio
                self._process_audio_chunk(audio_data)
                
        except Exception as e:
            print(f"Error in listening loop: {e}")
            
    def _process_audio_chunk(self, audio_data):
        """Process audio chunk for wake/sleep words and transcription"""
        try:
            # Skip processing if audio is too quiet (silence)
            if np.max(np.abs(audio_data)) < 0.005:
                return
                
            # Convert numpy array to WAV bytes
            wav_buffer = io.BytesIO()
            with wave.open(wav_buffer, 'wb') as wav_file:
                wav_file.setnchannels(self.channels)
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(self.rate)
                # Convert float32 to int16
                audio_int16 = (audio_data * 32767).astype(np.int16)
                wav_file.writeframes(audio_int16.tobytes())
            
            wav_buffer.seek(0)
            
            # Transcribe with Deepgram
            payload = {"buffer": wav_buffer.read()}
            options = PrerecordedOptions(
                model="nova-2",
                smart_format=True,
            )
            
            response = self.deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)
            
            # Extract text
            text = ""
            if response.results and response.results.channels:
                alternatives = response.results.channels[0].alternatives
                if alternatives:
                    text = alternatives[0].transcript.strip().lower()
            
            if not text:
                return
                
            print(f"Detected: {text}")
            
            # Check for wake/sleep words
            if not self.is_transcribing and self.wake_word in text:
                self.is_transcribing = True
                print(f"Wake word '{self.wake_word}' detected! Starting transcription...")
                if self.transcription_callback:
                    self.transcription_callback(f"[WAKE] Started transcription")
                    
            elif self.is_transcribing and self.sleep_word in text:
                self.is_transcribing = False
                print(f"Sleep word '{self.sleep_word}' detected! Stopping transcription...")
                if self.transcription_callback:
                    self.transcription_callback(f"[SLEEP] Stopped transcription")
                    
            elif self.is_transcribing:
                # Send transcription to callback
                original_text = alternatives[0].transcript.strip() if alternatives else ""
                if original_text and self.transcription_callback:
                    self.transcription_callback(original_text)
                    
        except Exception as e:
            print(f"Error processing audio: {e}")
    def __del__(self):
        """Cleanup"""
        self.stop_listening()