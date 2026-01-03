# Testing Guide

This document provides a comprehensive testing checklist for the Surveillance Camera Application.

## Pre-Testing Setup

1. Ensure Python 3.8+ is installed
2. Install all dependencies: `pip install -r requirements.txt`
3. Connect at least one USB camera to your computer
4. Ensure you have write permissions in your home directory

## Test Checklist

### 1. Installation & Launch Tests

- [ ] **Install dependencies**
  - Run: `pip install -r requirements.txt`
  - Verify: No errors during installation
  
- [ ] **Launch application (Method 1)**
  - Run: `python3 run.py`
  - Verify: Application launches without errors
  
- [ ] **Launch application (Method 2)**
  - Run: `python3 main.py`
  - Verify: Application launches without errors

### 2. Camera Detection Tests

- [ ] **Camera enumeration**
  - Click "Refresh Cameras"
  - Verify: All connected cameras are listed
  
- [ ] **No camera handling**
  - Disconnect all cameras
  - Click "Refresh Cameras"
  - Verify: "No cameras found" message appears
  - Verify: "Start Viewing" button is disabled
  
- [ ] **Camera reconnection**
  - With app running, connect a camera
  - Click "Refresh Cameras"
  - Verify: New camera appears in list

### 3. Video Display Tests

- [ ] **Start viewing**
  - Select a camera from dropdown
  - Click "Start Viewing"
  - Verify: Live video feed appears
  - Verify: Button changes to "Stop Viewing"
  - Verify: Camera dropdown becomes disabled
  
- [ ] **Stop viewing**
  - Click "Stop Viewing"
  - Verify: Video feed stops
  - Verify: Button changes to "Start Viewing"
  - Verify: Camera dropdown becomes enabled
  
- [ ] **FPS counter**
  - Start viewing
  - Verify: FPS counter updates in status bar
  - Verify: FPS is reasonable (>15 FPS)
  
- [ ] **Resolution test**
  - Open Settings
  - Try different resolutions (320x240, 640x480, 1280x720)
  - Restart viewing for each
  - Verify: Video displays correctly at each resolution

### 4. Motion Detection Tests

- [ ] **Enable motion detection**
  - Start viewing
  - Check "Enable Motion Detection"
  - Verify: Motion status shows "Motion: None"
  
- [ ] **Detect motion**
  - With motion detection enabled
  - Move something in front of camera
  - Verify: Green rectangles appear around moving objects
  - Verify: Status shows "Motion: Detected (N area(s))"
  - Verify: Status text turns red
  
- [ ] **Sensitivity adjustment**
  - Enable motion detection
  - Test sensitivity at 1 (low)
    - Verify: Only large movements detected
  - Test sensitivity at 100 (high)
    - Verify: Small movements detected
  - Test sensitivity at 50 (medium)
    - Verify: Normal movements detected
  
- [ ] **Disable motion detection**
  - Uncheck "Enable Motion Detection"
  - Move in front of camera
  - Verify: No rectangles appear
  - Verify: Status shows "Motion: Disabled"

### 5. Recording Tests

#### Continuous Recording

- [ ] **Start continuous recording**
  - Start viewing
  - Select "Continuous" mode
  - Check "Enable Recording"
  - Verify: Recording indicator turns red
  - Verify: Status shows "Recording: Active"
  
- [ ] **Stop continuous recording**
  - Uncheck "Enable Recording"
  - Verify: Recording indicator turns gray
  - Verify: Status shows "Recording: Off"
  - Verify: Video file exists in recordings directory
  - Verify: Video file can be played
  
- [ ] **Recording file format**
  - Record for 10 seconds
  - Stop recording
  - Check file: `~/SurveillanceRecordings/recording_YYYY-MM-DD_HH-MM-SS.mp4`
  - Verify: Filename has timestamp
  - Verify: File size is reasonable (>0 bytes)

#### Motion-Triggered Recording

- [ ] **Setup motion-triggered recording**
  - Start viewing
  - Enable motion detection
  - Select "Motion Triggered" mode
  - Check "Enable Recording"
  
- [ ] **Test motion trigger start**
  - Move in front of camera
  - Verify: Recording starts automatically
  - Verify: Recording indicator turns red
  
- [ ] **Test motion trigger stop**
  - Stop moving (stay still)
  - Wait for trigger duration (default 10 seconds)
  - Verify: Recording stops automatically
  - Verify: Recording indicator turns gray
  
- [ ] **Multiple motion events**
  - With motion-triggered recording enabled
  - Move, wait, move again
  - Verify: Recording continues through multiple motion events
  - Verify: Video file captures all motion events

### 6. Settings Tests

- [ ] **Open settings dialog**
  - Click "Settings" button
  - Verify: Settings dialog opens
  
- [ ] **Camera settings**
  - Change FPS (e.g., 15, 30, 60)
  - Change resolution
  - Click OK
  - Verify: Settings are saved
  - Restart viewing
  - Verify: New settings take effect
  
- [ ] **Recording path**
  - Open Settings
  - Click "Browse" for recording path
  - Select a different directory
  - Click OK
  - Start recording
  - Verify: Recording saves to new path
  
- [ ] **Video codec**
  - Open Settings
  - Try different codecs (mp4v, XVID)
  - Record test videos
  - Verify: Videos are playable
  
- [ ] **Motion trigger duration**
  - Open Settings
  - Set motion trigger duration to 5 seconds
  - Test motion-triggered recording
  - Verify: Recording stops 5 seconds after motion ends
  
- [ ] **Restore defaults**
  - Open Settings
  - Change several settings
  - Click "Restore Defaults"
  - Verify: All settings return to defaults

### 7. Error Handling Tests

- [ ] **Camera disconnection during viewing**
  - Start viewing
  - Disconnect camera (unplug USB)
  - Verify: Error message appears
  - Verify: Viewing stops gracefully
  
- [ ] **Recording to invalid path**
  - Open Settings
  - Set recording path to invalid location (e.g., `/invalid/path`)
  - Try to start recording
  - Verify: Error message appears
  - Verify: Recording doesn't start
  
- [ ] **Start recording without camera**
  - Don't start viewing
  - Try to enable recording
  - Verify: Error message appears
  - Verify: Recording checkbox unchecks
  
- [ ] **Multiple rapid starts/stops**
  - Rapidly click Start/Stop viewing 5 times
  - Verify: Application remains stable
  - Verify: No crashes or hangs

### 8. Performance Tests

- [ ] **Long-duration viewing**
  - Start viewing
  - Leave running for 5+ minutes
  - Verify: Video remains smooth
  - Verify: FPS stays consistent
  - Verify: No memory leaks (check system monitor)
  
- [ ] **Long-duration recording**
  - Start continuous recording
  - Record for 5+ minutes
  - Stop recording
  - Verify: File size is appropriate
  - Verify: Video plays correctly
  - Verify: No frame drops or corruption
  
- [ ] **Motion detection performance**
  - Enable motion detection
  - Run for 5+ minutes with constant motion
  - Verify: Application remains responsive
  - Verify: FPS doesn't degrade significantly

### 9. UI/UX Tests

- [ ] **Window resize**
  - Resize window to various sizes
  - Verify: Video scales appropriately
  - Verify: Controls remain accessible
  
- [ ] **Status bar updates**
  - Perform various actions
  - Verify: Status bar shows appropriate messages
  - Verify: Messages are clear and helpful
  
- [ ] **Button states**
  - Test all button enable/disable states
  - Verify: Buttons are disabled when action is invalid
  - Verify: Button text changes appropriately
  
- [ ] **Close application**
  - Close window while viewing
  - Verify: Camera stops cleanly
  - Verify: Recording stops if active
  - Verify: No hanging processes

### 10. Multi-Camera Tests (if available)

- [ ] **Switch between cameras**
  - Start viewing with Camera 0
  - Stop viewing
  - Select Camera 1
  - Start viewing
  - Verify: Correct camera is displayed
  
- [ ] **Different camera capabilities**
  - Test with cameras of different resolutions
  - Verify: Application adapts to each camera

## Test Results Template

Use this template to record your test results:

```
Test Date: _______________
OS: _______________
Python Version: _______________
Camera Model: _______________

| Test Category | Pass/Fail | Notes |
|---------------|-----------|-------|
| Installation  |           |       |
| Camera Detection |        |       |
| Video Display |           |       |
| Motion Detection |        |       |
| Recording     |           |       |
| Settings      |           |       |
| Error Handling |          |       |
| Performance   |           |       |
| UI/UX         |           |       |
| Multi-Camera  |           |       |

Issues Found:
1. 
2. 
3. 

Overall Result: PASS / FAIL
```

## Automated Testing

For developers, you can add automated tests using pytest:

```bash
pip install pytest pytest-qt
pytest tests/
```

(Note: Automated tests would need to be created separately)

## Performance Benchmarks

Expected performance metrics:
- FPS: >20 for 640x480, >15 for 1280x720
- Memory usage: <200MB during viewing
- CPU usage: <30% on modern hardware
- Recording overhead: <5% FPS drop

## Known Limitations

- Maximum tested recording duration: 2 hours
- Maximum tested file size: 5GB
- Simultaneous recordings: 1 at a time
- Motion detection: Best in controlled lighting

## Reporting Issues

When reporting issues, please include:
1. Operating system and version
2. Python version
3. Camera model
4. Steps to reproduce
5. Expected vs actual behavior
6. Error messages (if any)
7. Screenshots (if applicable)

