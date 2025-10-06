# Speech-to-Text Module with Wake/Sleep Word Detection

A modular speech-to-text system that activates transcription when a wake word is detected and stops when a sleep word is spoken.

## Features

- **Wake/Sleep Word Detection**: Toggles transcription with "hi"/"bye" commands
- **Real-time Transcription**: High-accuracy speech-to-text using Deepgram API
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
1. Say **"hi"** to start transcription
2. Speak normally - your words will appear
3. Say **"bye"** to stop transcription
4. Press **Ctrl+C** to exit

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



## Configuration

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

## License

This project is open source and available under the MIT License.