# Speech-to-Text Module with Wake/Sleep Word Detection

A modular speech-to-text system that activates transcription when a wake word is detected and stops when a sleep word is spoken.

## Features

- **True Wake/Sleep Word Detection**: Module activates transcription ONLY when "hi" is detected, stops when "bye" is spoken
- **Cost-Efficient**: No API calls when sleeping - only transcribes when awake
- **Real-time Transcription**: High-accuracy speech-to-text using Deepgram API when active
- **Modular Design**: Clean, reusable code structure
- **Cloud Processing**: Fast transcription with Deepgram's Nova-2 model

## Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Run the Project
```bash
# Desktop demo
python main.py

# Mobile bridge (for React Native)
python mobile_bridge.py
```

### Usage

**Desktop:**
1. Module starts in **SLEEP** mode (no transcription)
2. Say **"hi"** to **WAKE** the module and start transcription
3. Speak normally - your words will appear
4. Say **"bye"** to put module back to **SLEEP** (stops transcription)
5. Press **Ctrl+C** to exit

**React Native:**
1. Run `python mobile_bridge.py`
2. Use `ReactNativeExample.js` in your app
3. Connect to `ws://localhost:8765`

## Project Structure
```
speech-to-text-module/
├── main.py              # Entry point
├── demo.py              # Demo application
├── speech_module.py     # Core module
├── mobile_bridge.py     # React Native bridge
├── ReactNativeExample.js # Mobile app example
├── config.py            # Configuration
├── requirements.txt     # Dependencies
└── README.md           # Documentation
```



## How It Works

### Wake/Sleep States
- **SLEEP Mode**: Module listens only for wake word with minimal API usage
- **AWAKE Mode**: Full transcription active until sleep word detected
- **Cost Optimization**: ~80-90% reduction in API calls compared to always-on transcription

### Custom Wake/Sleep Words
```python
stt = SpeechToTextModule(wake_word="hello", sleep_word="goodbye")
```

## Configuration

Edit `config.py` to customize:
- API key
- Wake/sleep words
- Audio settings

## API Reference



## Dependencies

- `deepgram-sdk`: Speech recognition API
- `sounddevice`: Audio capture
- `numpy`: Audio processing
- `websockets`: WebSocket support








## Troubleshooting

### Audio Issues
- Ensure microphone permissions are granted
- Check audio device availability
- Verify sounddevice installation

### Setup
- Deepgram API key configured in config.py
- Free tier: 200 hours of transcription
- Internet connection required

## Output Video

https://github.com/user-attachments/assets/1328af11-5281-4d6d-83f8-471dc881423d

## License

This project is open source and available under the MIT License.
