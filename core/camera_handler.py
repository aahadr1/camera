"""Camera handling and video capture functionality."""
import cv2
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal, QMutex
from PyQt6.QtGui import QImage
from typing import List, Tuple, Optional


class CameraHandler(QThread):
    """Handles camera capture in a separate thread."""
    
    # Signals
    frame_ready = pyqtSignal(QImage, np.ndarray)  # QImage for display, ndarray for processing
    error_occurred = pyqtSignal(str)
    fps_updated = pyqtSignal(float)
    
    def __init__(self):
        """Initialize camera handler."""
        super().__init__()
        self.camera = None
        self.camera_index = 0
        self.running = False
        self.mutex = QMutex()
        self.frame_count = 0
        self.fps_timer = cv2.getTickCount()
    
    @staticmethod
    def enumerate_cameras(max_cameras: int = 10) -> List[Tuple[int, str]]:
        """Enumerate available camera devices.
        
        Args:
            max_cameras: Maximum number of camera indices to check
            
        Returns:
            List of tuples (index, name) for available cameras
        """
        available_cameras = []
        
        for i in range(max_cameras):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                # Try to read a frame to verify camera works
                ret, _ = cap.read()
                if ret:
                    # Try to get camera name (not always available)
                    backend_name = cap.getBackendName()
                    camera_name = f"Camera {i}"
                    
                    # Try to get more info
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    camera_name += f" ({width}x{height})"
                    
                    available_cameras.append((i, camera_name))
                cap.release()
        
        return available_cameras
    
    def set_camera(self, camera_index: int) -> bool:
        """Set the camera to use.
        
        Args:
            camera_index: Index of the camera to use
            
        Returns:
            True if camera was set successfully, False otherwise
        """
        self.mutex.lock()
        
        # Release current camera if any
        if self.camera is not None:
            self.camera.release()
            self.camera = None
        
        # Open new camera
        self.camera_index = camera_index
        self.camera = cv2.VideoCapture(camera_index)
        
        if not self.camera.isOpened():
            self.mutex.unlock()
            self.error_occurred.emit(f"Failed to open camera {camera_index}")
            return False
        
        # Set camera properties for better performance
        self.camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        self.mutex.unlock()
        return True
    
    def set_resolution(self, width: int, height: int) -> None:
        """Set camera resolution.
        
        Args:
            width: Frame width
            height: Frame height
        """
        if self.camera is not None:
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    def set_fps(self, fps: int) -> None:
        """Set camera FPS.
        
        Args:
            fps: Frames per second
        """
        if self.camera is not None:
            self.camera.set(cv2.CAP_PROP_FPS, fps)
    
    def run(self) -> None:
        """Main thread loop for capturing frames."""
        self.running = True
        consecutive_failures = 0
        max_failures = 30  # Stop after 30 consecutive failures
        
        while self.running:
            self.mutex.lock()
            
            if self.camera is None or not self.camera.isOpened():
                self.mutex.unlock()
                self.error_occurred.emit("Camera not available")
                break
            
            ret, frame = self.camera.read()
            self.mutex.unlock()
            
            if not ret:
                consecutive_failures += 1
                if consecutive_failures >= max_failures:
                    self.error_occurred.emit("Camera disconnected or failed")
                    break
                elif consecutive_failures == 1:
                    self.error_occurred.emit("Failed to read frame from camera")
                continue
            
            # Reset failure counter on successful read
            consecutive_failures = 0
            
            # Calculate FPS
            self.frame_count += 1
            if self.frame_count % 30 == 0:
                current_time = cv2.getTickCount()
                fps = 30.0 / ((current_time - self.fps_timer) / cv2.getTickFrequency())
                self.fps_timer = current_time
                self.fps_updated.emit(fps)
            
            # Convert frame to QImage for display
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            
            # Emit both QImage (for display) and numpy array (for processing)
            self.frame_ready.emit(qt_image.copy(), frame.copy())
        
        # Cleanup
        self.mutex.lock()
        if self.camera is not None:
            self.camera.release()
            self.camera = None
        self.mutex.unlock()
    
    def stop(self) -> None:
        """Stop the camera capture thread."""
        self.running = False
        self.wait()  # Wait for thread to finish
    
    def get_current_frame_size(self) -> Optional[Tuple[int, int]]:
        """Get current frame size.
        
        Returns:
            Tuple of (width, height) or None if camera not available
        """
        if self.camera is not None and self.camera.isOpened():
            width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
            return (width, height)
        return None

