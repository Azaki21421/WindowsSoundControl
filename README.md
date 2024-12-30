# WindowsSoundControl

A simple Python application that allows you to manage and monitor the audio volume of applications running on your system. It provides features to:
- Monitor the volume levels of applications.
- Save and apply custom volume settings for each application.
- Display the current volumes in a system tray icon.
- Provide an interface to add or update volume settings for specific applications.

## Features
- **Monitor Volumes**: Continuously monitors the volume levels of running applications and system sounds.
- **Save and Apply Settings**: Save volume settings to a file and apply them to the applications.
- **System Tray Icon**: A system tray icon that allows easy access to features like showing current volumes, saving volumes, and adjusting volumes for specific applications.
- **Add/Update Volume**: Allows users to manually set volume levels for specific applications.

## Requirements

This project requires Python 3 and the following Python libraries:

- `pycaw`: To control and get the audio volume for applications.
- `comtypes`: For handling COM interfaces used by `pycaw`.
- `pystray`: For creating a system tray icon.
- `Pillow`: For creating and manipulating the tray icon image.
- `tk`: For displaying dialogs to show and update volume settings.

To install the required dependencies, you can use the following command:

```bash
pip install -r requirements.txt
```

# Usage

1. Clone this repository:

```bash
git clone https://github.com/Azaki21421/WindowsSoundControl.git
cd WindowsSoundControl
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python sound_control.py
```

4. A system tray icon will appear. Right-click the icon to access the following options:

- Show Current Volumes: Display the current volumes of all applications.
- Save Current Volumes: Save the current volume levels to a file.
- Apply Volume Settings: Apply previously saved volume settings.
- Add/Update Volume: Manually set the volume level for a specific application.
- Exit: Close the application.

# Configuration
The application saves volume settings in a JSON file (volume_settings.json). The settings are automatically loaded when the application starts and can be updated through the system tray menu.
