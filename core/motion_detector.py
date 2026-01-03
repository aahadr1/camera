"""Motion detection functionality."""
import cv2
import numpy as np
from PyQt6.QtCore import QObject, pyqtSignal
from typing import List, Tuple


class MotionDetector(QObject):
    """Detects motion in video frames."""
    
    # Signals
    motion_detected = pyqtSignal(bool, list)  # bool: motion detected, list: bounding boxes
    
    def __init__(self, sensitivity: int = 50):
        """Initialize motion detector.
        
        Args:
            sensitivity: Motion detection sensitivity (1-100)
        """
        super().__init__()
        self.sensitivity = sensitivity
        self.enabled = False
        self.previous_frame = None
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500,
            varThreshold=16,
            detectShadows=True
        )
        
    def set_sensitivity(self, sensitivity: int) -> None:
        """Set motion detection sensitivity.
        
        Args:
            sensitivity: Sensitivity value (1-100)
        """
        self.sensitivity = max(1, min(100, sensitivity))
        # Adjust background subtractor threshold based on sensitivity
        # Lower sensitivity = higher threshold (less sensitive)
        threshold = int(50 - (self.sensitivity - 50) * 0.5)
        self.background_subtractor.setVarThreshold(max(5, threshold))
    
    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable motion detection.
        
        Args:
            enabled: True to enable, False to disable
        """
        self.enabled = enabled
        if not enabled:
            self.previous_frame = None
    
    def process_frame(self, frame: np.ndarray) -> Tuple[bool, List[Tuple[int, int, int, int]], np.ndarray]:
        """Process a frame for motion detection.
        
        Args:
            frame: Input frame (BGR format)
            
        Returns:
            Tuple of (motion_detected, bounding_boxes, processed_frame)
            bounding_boxes: List of (x, y, width, height) tuples
        """
        if not self.enabled:
            return False, [], frame
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        # Initialize previous frame if needed
        if self.previous_frame is None:
            self.previous_frame = gray
            return False, [], frame
        
        # Compute absolute difference between current and previous frame
        frame_delta = cv2.absdiff(self.previous_frame, gray)
        
        # Threshold the delta image
        # Sensitivity affects the threshold value
        threshold_value = int(25 + (100 - self.sensitivity) * 0.5)
        thresh = cv2.threshold(frame_delta, threshold_value, 255, cv2.THRESH_BINARY)[1]
        
        # Dilate the thresholded image to fill in holes
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        # Find contours
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by area (minimum size)
        min_area = 500 / (self.sensitivity / 50)  # Adjust minimum area based on sensitivity
        bounding_boxes = []
        motion_detected = False
        
        result_frame = frame.copy()
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < min_area:
                continue
            
            motion_detected = True
            (x, y, w, h) = cv2.boundingRect(contour)
            bounding_boxes.append((x, y, w, h))
            
            # Draw rectangle on frame
            cv2.rectangle(result_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Update previous frame
        self.previous_frame = gray
        
        # Emit signal
        self.motion_detected.emit(motion_detected, bounding_boxes)
        
        return motion_detected, bounding_boxes, result_frame
    
    def reset(self) -> None:
        """Reset motion detector state."""
        self.previous_frame = None
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500,
            varThreshold=16,
            detectShadows=True
        )

