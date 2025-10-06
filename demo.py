#!/usr/bin/env python3
"""
Demo script for Speech-to-Text Module with Wake/Sleep Word Detection
"""

import time
from speech_module import SpeechToTextModule
from config import WAKE_WORD, SLEEP_WORD

def transcription_handler(text):
    """Handle transcription results"""
    timestamp = time.strftime("%H:%M:%S")
    
    if "[WAKE]" in text:
        print(f"\n>>> {timestamp} - WAKE WORD DETECTED! Transcription started <<<")
    elif "[SLEEP]" in text:
        print(f">>> {timestamp} - SLEEP WORD DETECTED! Transcription stopped <<<\n")
    else:
        print(f"[{timestamp}] {text}")

def main():
    print("=" * 60)
    print("SPEECH-TO-TEXT MODULE DEMO")
    print("=" * 60)
    print(f"Wake word: '{WAKE_WORD}'")
    print(f"Sleep word: '{SLEEP_WORD}'")
    print("Press Ctrl+C to exit")
    print("=" * 60)
    
    # Initialize the speech module
    stt_module = SpeechToTextModule()
    stt_module.set_transcription_callback(transcription_handler)
    
    try:
        stt_module.start_listening()
        print(f"\nListening for wake word '{WAKE_WORD}'...")
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        stt_module.stop_listening()
        print("Demo completed successfully!")

if __name__ == "__main__":
    main()