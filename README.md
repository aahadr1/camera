# USB Camera Surveillance Application

A professional cross-platform surveillance camera application built with Python, PyQt6, and OpenCV. Perfect for home security, baby monitoring, or any surveillance needs.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

## Features

### Core Functionality
- **USB Camera Support**: Connect and view multiple USB cameras/webcams
- **Live Video Display**: Real-time camera feed with smooth 30 FPS viewing
- **Camera Selection**: Easy switching between multiple connected cameras
- **High DPI Support**: Looks great on modern displays

### Motion Detection
- **Intelligent Detection**: Advanced motion detection using background subtraction
- **Visual Feedback**: Green bounding boxes highlight motion areas
- **Adjustable Sensitivity**: Fine-tune detection (1-100 scale)
- **Real-time Status**: Instant motion alerts in the interface

### Video Recording
- **Continuous Mode**: Record everything while enabled
- **Motion-Triggered Mode**: Save disk space by recording only when motion is detected
- **Automatic Naming**: Files timestamped for easy organization
- **Multiple Codecs**: Support for MP4V, XVID, H.264, and MJPEG

### Configuration
- **Persistent Settings**: Your preferences are saved automatically
- **Flexible Resolution**: Support from 320x240 to 1920x1080
- **Custom Recording Path**: Save recordings anywhere you want
- **FPS Control**: Optimize performance for your hardware

## Screenshots

```
┌─────────────────────────────────────────────────────┐
│ Surveillance Camera Viewer                    [_][□][×]│
├─────────────────────────────────────────────────────┤
│ Camera: Camera 0 (640x480)      [Refresh Cameras] │
├─────────────────────────────────────────────────────┤
│                                                     │
│                                                     │
│                  [Live Video Feed]                  │
│                   (640x480)                         │
│                                                     │
│                                                     │
├─────────────────────────────────────────────────────┤
│         [Start Viewing]              [Settings]    │
├─────────────────────────────────────────────────────┤
│ ☑ Enable Motion Detection   Sensitivity: [▓▓▓░░] 60│
│ ☑ Enable Recording  Mode: [Motion Triggered ▼] ●  │
├─────────────────────────────────────────────────────┤
│ FPS: 29.8 | Motion: Detected (2 areas) | Recording: Active │
└─────────────────────────────────────────────────────┘
```

## Requirements

- **Python**: 3.8 or higher
- **Hardware**: Any UVC-compatible USB webcam
- **OS**: Windows 7+, macOS 10.13+, or Linux
- **RAM**: 2GB minimum, 4GB recommended
- **Disk**: 100MB for app + space for recordings

## Quick Start

### 1. Check System Compatibility

```bash
python3 check_system.py
```

This will verify your system has everything needed.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install packages individually:
```bash
pip install PyQt6 opencv-python numpy
```

### 3. Run the Application

**Recommended** (with dependency checking):
```bash
python3 run.py
```

**Direct** execution:
```bash
python3 main.py
```

### 4. Start Monitoring

1. Connect your USB camera
2. Select camera from dropdown
3. Click "Start Viewing"
4. Enable features as needed

## Documentation

- **[Quick Start Guide](QUICKSTART.md)**: Get up and running in 5 minutes
- **[Testing Guide](TESTING.md)**: Comprehensive testing checklist
- **[System Check](check_system.py)**: Verify your installation

## Usage Examples

### Home Security Monitoring
```
1. Mount camera at entry point
2. Enable motion detection (sensitivity ~70)
3. Enable motion-triggered recording
4. Leave running 24/7
```

### Baby Monitor
```
1. Position camera to view crib
2. Enable continuous recording
3. Adjust sensitivity low (~30) to avoid false alarms
4. Use high resolution for clarity
```

### Wildlife Camera
```
1. Position camera at window/feeder
2. Enable motion-triggered recording
3. Set high sensitivity (~80)
4. Use low resolution to save space
```

## Configuration

### Default Settings

| Setting | Default Value | Description |
|---------|---------------|-------------|
| Resolution | 640x480 | Camera capture resolution |
| FPS | 30 | Frames per second |
| Motion Sensitivity | 50 | Detection sensitivity (1-100) |
| Recording Path | ~/SurveillanceRecordings | Where videos are saved |
| Video Codec | mp4v | Video compression format |
| Trigger Duration | 10s | Recording continues after motion stops |

### Customization

Open **Settings** to customize:
- Camera resolution and FPS
- Recording directory and codec
- Motion detection sensitivity
- Motion trigger duration

All settings are saved automatically.

## File Organization

```
camera/
├── main.py                    # Application entry point
├── run.py                     # Launcher with dependency check
├── check_system.py            # System verification utility
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── QUICKSTART.md             # Quick start guide
├── TESTING.md                # Testing documentation
├── ui/
│   ├── main_window.py        # Main application window
│   └── settings_dialog.py    # Settings configuration
├── core/
│   ├── camera_handler.py     # Camera capture and threading
│   ├── motion_detector.py    # Motion detection logic
│   └── video_recorder.py     # Video recording functionality
└── utils/
    └── config.py             # Configuration management
```

## Troubleshooting

### No Cameras Detected

**macOS:**
```bash
# Grant camera permissions
System Preferences → Security & Privacy → Camera
```

**Linux:**
```bash
# Check camera device
ls -l /dev/video*

# Add user to video group
sudo usermod -a -G video $USER
```

**Windows:**
```
Settings → Privacy → Camera → Allow apps to access camera
```

### Poor Performance

- Reduce resolution in Settings (try 320x240)
- Lower FPS to 15
- Disable motion detection when not needed
- Close other camera applications
- Check CPU usage in Task Manager

### Recording Issues

- Verify disk space is available
- Check recording path exists and is writable
- Try different video codec in Settings
- Ensure camera is providing stable feed

### Application Won't Start

```bash
# Verify Python version
python3 --version  # Should be 3.8+

# Check dependencies
python3 check_system.py

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

## Advanced Usage

### Command Line Options

The application currently runs with GUI only. Command-line options may be added in future versions.

### Multiple Camera Setup

To monitor multiple cameras:
1. Run separate instances of the application
2. Select different cameras in each instance
3. Configure different recording paths in Settings

### Performance Optimization

For best performance:
- **Low-end hardware**: 320x240 @ 15 FPS
- **Mid-range hardware**: 640x480 @ 30 FPS  
- **High-end hardware**: 1280x720 @ 30 FPS

## Contributing

Contributions are welcome! Areas for improvement:
- Additional video codecs
- Email/SMS notifications
- Multi-camera grid view
- Scheduled recording
- Cloud storage integration

## Known Limitations

- Single camera recording at a time
- No audio recording (video only)
- Motion detection works best in controlled lighting
- Maximum tested recording duration: 2 hours continuous

## Support

For issues or questions:
1. Check [QUICKSTART.md](QUICKSTART.md)
2. Run `python3 check_system.py`
3. Review [TESTING.md](TESTING.md)
4. Check error messages in terminal

## Credits

Built with:
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - GUI framework
- [OpenCV](https://opencv.org/) - Computer vision library
- [NumPy](https://numpy.org/) - Numerical computing

## License

MIT License - feel free to use for personal or commercial projects.

## Version History

- **v1.0.0** (2026-01-03)
  - Initial release
  - Camera viewing and selection
  - Motion detection
  - Video recording (continuous and motion-triggered)
  - Settings configuration
  - Cross-platform support

---

**Made with ❤️ for surveillance and monitoring needs**

# camera
# cam-app-2
