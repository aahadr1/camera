# Quick Start Guide

## Installation

1. **Install Python 3.8 or higher**
   - Check your Python version: `python3 --version`

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install individually:
   ```bash
   pip install PyQt6 opencv-python numpy
   ```

## Running the Application

### Option 1: Using the launcher script (recommended)
```bash
python3 run.py
```

### Option 2: Direct execution
```bash
python3 main.py
```

## First Time Setup

1. **Connect your USB camera** to your computer

2. **Launch the application** using one of the methods above

3. **Select your camera**:
   - Click "Refresh Cameras" to scan for connected cameras
   - Select your camera from the dropdown menu

4. **Start viewing**:
   - Click "Start Viewing" to see the live camera feed

## Features

### Motion Detection
1. Check "Enable Motion Detection"
2. Adjust sensitivity slider (1-100)
   - Lower values: Less sensitive (larger movements needed)
   - Higher values: More sensitive (detects smaller movements)
3. Motion areas will be highlighted with green rectangles

### Recording

#### Continuous Recording
1. Check "Enable Recording"
2. Select "Continuous" mode
3. Video will record continuously while enabled

#### Motion-Triggered Recording
1. Check "Enable Recording"
2. Select "Motion Triggered" mode
3. Enable "Motion Detection"
4. Recording starts automatically when motion is detected
5. Recording continues for 10 seconds after motion stops (configurable in settings)

### Settings

Click the "Settings" button to configure:
- **Camera Settings**: FPS, Resolution
- **Recording Settings**: Save path, video codec, motion trigger duration
- **Motion Detection**: Default sensitivity

## Recordings Location

By default, recordings are saved to:
```
~/SurveillanceRecordings/
```

Files are named with timestamps:
```
recording_YYYY-MM-DD_HH-MM-SS.mp4
```

## Troubleshooting

### No cameras detected
- Ensure your camera is properly connected
- Try unplugging and reconnecting the camera
- Check if other applications are using the camera
- On macOS: Grant camera permissions in System Preferences
- On Linux: Check camera permissions (`ls -l /dev/video*`)

### Camera permission denied
- **macOS**: System Preferences → Security & Privacy → Camera
- **Linux**: Add user to video group: `sudo usermod -a -G video $USER`
- **Windows**: Settings → Privacy → Camera

### Poor performance
- Reduce camera resolution in Settings
- Lower the FPS in Settings
- Close other applications using the camera
- Disable motion detection if not needed

### Recording issues
- Check disk space
- Verify the recording path exists and is writable
- Try changing the video codec in Settings

## Keyboard Shortcuts

- **Esc**: Stop viewing (when window has focus)

## Tips

1. **For best motion detection**:
   - Mount the camera in a stable position
   - Adjust sensitivity based on your environment
   - Test different lighting conditions

2. **For surveillance use**:
   - Use motion-triggered recording to save disk space
   - Regularly check the recording directory
   - Consider setting up automatic cleanup of old recordings

3. **Multiple cameras**:
   - Stop viewing before switching cameras
   - Each camera may have different optimal settings

## System Requirements

- **OS**: Windows 7+, macOS 10.13+, or Linux
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum, 4GB recommended
- **Disk Space**: 100MB for application, varies for recordings
- **Camera**: Any USB webcam or camera (UVC compatible)

## Support

For issues or questions, please check:
1. This guide's troubleshooting section
2. The main README.md file
3. Application logs (displayed in terminal when running)

---

**Enjoy your surveillance camera system!**

