# Voice to Automation

A macOS menubar app that uses voice commands to automate tasks in Ableton Live and other applications.

## Features

- Voice-controlled workflow automation
- Easy-to-use macOS menubar interface
- Easily extensible for different applications
- Low resource consumption
- Currently focused on Ableton Live integration

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Picovoice AccessKey:
   ```
   ACCESS_KEY=your_access_key_here
   ```
4. Run the app with:
   ```
   python vta.py
   ```

## Usage

1. Click the menubar icon and select "Microphone On" to start voice recognition
2. Make sure your target application (like Ableton Live) is the focused application
3. Speak commands to execute predefined actions
4. The app will automatically perform the requested tasks

## Ableton Live Integration

The app currently has robust integration with Ableton Live:
- Load plugins by voice (e.g., "Serum", "EQ8", "OTT")
- Navigate Ableton's interface with voice commands
- Trigger common actions through speech

## Extensibility

The command structure is defined in JSON files, making it easy to add new applications or extend functionality:
- Modify expressions.json to customize Ableton commands
- Create new JSON definition files for other applications

## Building the Application

To build a standalone macOS application:

```
python setup.py py2app
```

## Requirements

- macOS
- Python 3.6+
- Picovoice AccessKey (for voice recognition)

## License

MIT