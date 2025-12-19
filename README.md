# GestureMidi - Hand Gesture Controlled DJ System

A Python-based hand gesture controlled DJ system that uses computer vision to track hand movements and translates them into MIDI signals for controlling DJ software.

## Features

- Real-time hand tracking using MediaPipe
- MIDI output for seamless integration with DJ software
- Support for dual-hand control (left and right hands)
- Visual feedback on screen showing current gestures
- Customizable gesture mappings for different DJ controls

## Requirements

- Python 3.7+
- Webcam
- Virtual MIDI port (platform-specific setup required)
- DJ software that supports MIDI input (e.g., Mixxx, Traktor, Serato)

## Installation

1. Clone or download the repository
2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install opencv-python mediapipe mido python-rtmidi
```

## Setup

### MIDI Port Setup

Before running the application, you need to set up a virtual MIDI port:

- **macOS**: Enable the IAC Driver in Audio MIDI Setup
- **Windows**: Install and configure loopMIDI
- **Linux**: Use ALSA virtual MIDI ports

### DJ Software Configuration

1. Open your preferred DJ software
2. Configure it to receive MIDI input from the virtual port
3. Use MIDI Learn functionality to map the controls:
   - CC 1/11: Volume (Left/Right deck)
   - CC 2/12: Low EQ
   - CC 3/13: Mid EQ
   - CC 4/14: High EQ
   - Note 60/70: Play button

## Usage

Run the application:

```bash
python GestureMidi.py
```

### Gesture Controls

Position your hands in front of the webcam. The application will display gesture recognition on screen.

#### Left Hand Gestures:
- ✊ **Fist**: No action
- 🖐 **Open hand with thumb out**: Play (debounced to prevent accidental triggers)
- 🤙 **Thumb + pinky**: Control Volume
- 🤘 **Pinky only**: Control Low EQ
- ☝️ **Index finger only**: Control Mid EQ
- ✌️ **Index + middle fingers**: Control High EQ

#### Right Hand Gestures:
Same as left hand, but controls the right deck (offset MIDI channels).

### Visual Feedback

The application displays current gesture status in the top-left corner:
- L: [GESTURE] - Left hand status
- R: [GESTURE] - Right hand status

## Supported DJ Software

- **Mixxx** (Free, open-source): https://mixxx.org/
- **Traktor Pro**
- **Serato DJ**
- **Virtual DJ**
- Any DJ software with MIDI mapping support

## Troubleshooting

### No MIDI ports found
- Ensure virtual MIDI driver is installed and enabled
- Restart your computer after installing MIDI drivers
- Check Audio MIDI Setup (macOS) or MIDI settings

### Hand not detected
- Ensure good lighting
- Position hands clearly in camera view
- Adjust camera angle for better detection
- Try different hand positions

### Gestures not responding
- Verify DJ software is configured to receive MIDI
- Check MIDI port selection in DJ software
- Ensure gesture is clearly formed and detected

### Performance issues
- Close other applications using the camera
- Reduce camera resolution if needed
- Ensure sufficient CPU/GPU resources

## Dependencies

- `opencv-python`: Computer vision and camera handling
- `mediapipe`: Hand tracking and pose estimation
- `mido`: MIDI message handling
- `python-rtmidi`: MIDI backend for mido

## License

This project is open-source. Feel free to modify and distribute.

## Contributing

Contributions welcome! Please submit issues and pull requests on GitHub.