"""Video recording functionality."""
import cv2
import numpy as np
from datetime import datetime
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from typing import Optional


class VideoRecorder(QObject):
    """Handles video recording with multiple modes."""
    
    # Signals
    recording_started = pyqtSignal(str)  # filename
    recording_stopped = pyqtSignal()
    recording_error = pyqtSignal(str)
    
    def __init__(self, output_path: str, codec: str = 'mp4v', fps: int = 30):
        """Initialize video recorder.
        
        Args:
            output_path: Directory to save recordings
            codec: Video codec (e.g., 'mp4v', 'XVID')
            fps: Frames per second for recording
        """
        super().__init__()
        self.output_path = Path(output_path)
        self.codec = codec
        self.fps = fps
        self.writer = None
        self.current_filename = None
        self.is_recording = False
        self.recording_mode = 'continuous'  # 'continuous' or 'motion_triggered'
        self.motion_trigger_duration = 10  # seconds
        self.motion_stop_timer = None
        self.frame_size = None
    
    def set_output_path(self, path: str) -> None:
        """Set output directory for recordings.
        
        Args:
            path: Directory path
        """
        self.output_path = Path(path)
        self.output_path.mkdir(parents=True, exist_ok=True)
    
    def set_recording_mode(self, mode: str) -> None:
        """Set recording mode.
        
        Args:
            mode: 'continuous' or 'motion_triggered'
        """
        self.recording_mode = mode
    
    def set_motion_trigger_duration(self, duration: int) -> None:
        """Set duration to continue recording after motion stops.
        
        Args:
            duration: Duration in seconds
        """
        self.motion_trigger_duration = duration
    
    def start_recording(self, frame_size: tuple) -> bool:
        """Start recording video.
        
        Args:
            frame_size: Tuple of (width, height)
            
        Returns:
            True if recording started successfully
        """
        if self.is_recording:
            return True
        
        try:
            # Ensure output directory exists and is writable
            self.output_path.mkdir(parents=True, exist_ok=True)
            
            # Test write permissions
            test_file = self.output_path / ".write_test"
            try:
                test_file.touch()
                test_file.unlink()
            except (PermissionError, OSError) as e:
                self.recording_error.emit(f"Recording directory not writable: {str(e)}")
                return False
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.current_filename = self.output_path / f"recording_{timestamp}.mp4"
            
            # Create video writer
            fourcc = cv2.VideoWriter_fourcc(*self.codec)
            self.writer = cv2.VideoWriter(
                str(self.current_filename),
                fourcc,
                self.fps,
                frame_size
            )
            
            if not self.writer.isOpened():
                self.recording_error.emit("Failed to open video writer")
                return False
            
            self.is_recording = True
            self.frame_size = frame_size
            self.recording_started.emit(str(self.current_filename))
            return True
            
        except Exception as e:
            self.recording_error.emit(f"Error starting recording: {str(e)}")
            return False
    
    def stop_recording(self) -> None:
        """Stop recording video."""
        if not self.is_recording:
            return
        
        if self.writer is not None:
            self.writer.release()
            self.writer = None
        
        self.is_recording = False
        self.current_filename = None
        self.recording_stopped.emit()
        
        # Cancel motion stop timer if active
        if self.motion_stop_timer is not None:
            self.motion_stop_timer.stop()
            self.motion_stop_timer = None
    
    def write_frame(self, frame: np.ndarray) -> None:
        """Write a frame to the video file.
        
        Args:
            frame: Frame to write (BGR format)
        """
        if self.is_recording and self.writer is not None:
            try:
                self.writer.write(frame)
            except Exception as e:
                self.recording_error.emit(f"Error writing frame: {str(e)}")
    
    def handle_motion_detected(self, motion_detected: bool, frame: np.ndarray) -> None:
        """Handle motion detection for motion-triggered recording.
        
        Args:
            motion_detected: True if motion was detected
            frame: Current frame
        """
        if self.recording_mode != 'motion_triggered':
            return
        
        frame_h, frame_w = frame.shape[:2]
        frame_size = (frame_w, frame_h)
        
        if motion_detected:
            # Start recording if not already recording
            if not self.is_recording:
                self.start_recording(frame_size)
            
            # Cancel stop timer if active
            if self.motion_stop_timer is not None:
                self.motion_stop_timer.stop()
                self.motion_stop_timer = None
            
            # Write frame
            self.write_frame(frame)
        else:
            # Motion stopped - start timer to stop recording
            if self.is_recording:
                if self.motion_stop_timer is None:
                    self.motion_stop_timer = QTimer()
                    self.motion_stop_timer.timeout.connect(self.stop_recording)
                    self.motion_stop_timer.setSingleShot(True)
                    self.motion_stop_timer.start(self.motion_trigger_duration * 1000)
                
                # Continue writing frames until timer expires
                self.write_frame(frame)
    
    def is_recording_active(self) -> bool:
        """Check if currently recording.
        
        Returns:
            True if recording is active
        """
        return self.is_recording
    
    def get_current_filename(self) -> Optional[str]:
        """Get current recording filename.
        
        Returns:
            Current filename or None if not recording
        """
        return str(self.current_filename) if self.current_filename else None

