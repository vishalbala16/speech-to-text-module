#!/usr/bin/env python3
"""
CORRECT Demo: Module only transcribes when AWAKE (between 'hi' and 'bye')
"""

import time
from speech_module import SpeechToTextModule
from config import WAKE_WORD, SLEEP_WORD

def transcription_handler(text):
    """Handle transcription results"""
    timestamp = time.strftime("%H:%M:%S")
    
    if "[WAKE]" in text:
        print(f"\n[WAKE] [{timestamp}] {text}")
    elif "[SLEEP]" in text:
        print(f"[SLEEP] [{timestamp}] {text}\n")
    else:
        print(f"[TRANSCRIPT] [{timestamp}] {text}")

def main():
    print("=" * 70)
    print("CORRECT SPEECH-TO-TEXT MODULE - WAKE/SLEEP IMPLEMENTATION")
    print("=" * 70)
    print(f"Wake word: '{WAKE_WORD}' - Activates transcription")
    print(f"Sleep word: '{SLEEP_WORD}' - Deactivates transcription")
    print("[SLEEP] Module starts in SLEEP mode (no transcription)")
    print("Press Ctrl+C to exit")
    print("=" * 70)
    
    # Initialize correct speech module
    stt_module = SpeechToTextModule()
    stt_module.set_transcription_callback(transcription_handler)
    
    try:
        stt_module.start_listening()
        print(f"\n[SLEEP] SLEEPING - Say '{WAKE_WORD}' to activate transcription...")
        
        while True:
            time.sleep(2)
            status = stt_module.get_status()
            if status == "AWAKE":
                print(f"[AWAKE] Status: {status} - Transcribing... (say '{SLEEP_WORD}' to stop)")
            else:
                print(f"[SLEEP] Status: {status} - Waiting for '{WAKE_WORD}'...")
            
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        stt_module.stop_listening()
        print("Demo completed!")

if __name__ == "__main__":
    main()