"""Main application window."""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QSlider, QCheckBox, QStatusBar,
    QGroupBox, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSlot, QSize
from PyQt6.QtGui import QPixmap, QImage, QPalette, QColor
import numpy as np

from core.camera_handler import CameraHandler
from core.motion_detector import MotionDetector
from core.video_recorder import VideoRecorder
from utils.config import Config


class MainWindow(QMainWindow):
    """Main application window for surveillance camera."""
    
    def __init__(self, config: Config):
        """Initialize main window.
        
        Args:
            config: Configuration manager
        """
        super().__init__()
        self.config = config
        
        # Initialize components
        self.camera_handler = CameraHandler()
        self.motion_detector = MotionDetector(config.get('motion_sensitivity'))
        self.video_recorder = VideoRecorder(
            config.ensure_recording_path(),
            config.get('video_codec'),
            config.get('fps')
        )
        
        # State
        self.current_frame = None
        self.is_viewing = False
        
        # Setup UI
        self.setup_ui()
        self.connect_signals()
        self.load_settings()
        
        # Window properties
        self.setWindowTitle("Surveillance Camera Viewer")
        self.setMinimumSize(QSize(900, 700))
    
    def setup_ui(self) -> None:
        """Setup the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # Camera selection group
        camera_group = QGroupBox("Camera Selection")
        camera_layout = QHBoxLayout()
        
        self.camera_combo = QComboBox()
        self.refresh_cameras_btn = QPushButton("Refresh Cameras")
        self.refresh_cameras_btn.clicked.connect(self.refresh_cameras)
        
        camera_layout.addWidget(QLabel("Camera:"))
        camera_layout.addWidget(self.camera_combo, stretch=1)
        camera_layout.addWidget(self.refresh_cameras_btn)
        camera_group.setLayout(camera_layout)
        main_layout.addWidget(camera_group)
        
        # Video display
        video_group = QGroupBox("Live View")
        video_layout = QVBoxLayout()
        
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setMinimumSize(QSize(640, 480))
        self.video_label.setStyleSheet("QLabel { background-color: black; }")
        self.video_label.setScaledContents(False)
        
        video_layout.addWidget(self.video_label)
        video_group.setLayout(video_layout)
        main_layout.addWidget(video_group, stretch=1)
        
        # Control buttons
        control_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("Start Viewing")
        self.start_btn.clicked.connect(self.toggle_viewing)
        self.start_btn.setMinimumHeight(40)
        
        self.settings_btn = QPushButton("Settings")
        self.settings_btn.clicked.connect(self.show_settings)
        self.settings_btn.setMinimumHeight(40)
        
        control_layout.addWidget(self.start_btn, stretch=1)
        control_layout.addWidget(self.settings_btn)
        main_layout.addLayout(control_layout)
        
        # Features group
        features_group = QGroupBox("Features")
        features_layout = QVBoxLayout()
        
        # Motion detection
        motion_layout = QHBoxLayout()
        self.motion_check = QCheckBox("Enable Motion Detection")
        self.motion_check.toggled.connect(self.toggle_motion_detection)
        motion_layout.addWidget(self.motion_check)
        
        motion_layout.addWidget(QLabel("Sensitivity:"))
        self.sensitivity_slider = QSlider(Qt.Orientation.Horizontal)
        self.sensitivity_slider.setMinimum(1)
        self.sensitivity_slider.setMaximum(100)
        self.sensitivity_slider.setValue(50)
        self.sensitivity_slider.valueChanged.connect(self.update_sensitivity)
        motion_layout.addWidget(self.sensitivity_slider, stretch=1)
        
        self.sensitivity_label = QLabel("50")
        motion_layout.addWidget(self.sensitivity_label)
        
        features_layout.addLayout(motion_layout)
        
        # Recording
        recording_layout = QHBoxLayout()
        self.recording_check = QCheckBox("Enable Recording")
        self.recording_check.toggled.connect(self.toggle_recording)
        recording_layout.addWidget(self.recording_check)
        
        self.recording_mode_combo = QComboBox()
        self.recording_mode_combo.addItems(["Continuous", "Motion Triggered"])
        self.recording_mode_combo.currentTextChanged.connect(self.update_recording_mode)
        recording_layout.addWidget(QLabel("Mode:"))
        recording_layout.addWidget(self.recording_mode_combo)
        
        self.recording_indicator = QLabel("●")
        self.recording_indicator.setStyleSheet("QLabel { color: gray; font-size: 20px; }")
        recording_layout.addWidget(self.recording_indicator)
        
        recording_layout.addStretch()
        features_layout.addLayout(recording_layout)
        
        features_group.setLayout(features_layout)
        main_layout.addWidget(features_group)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.fps_label = QLabel("FPS: 0.0")
        self.motion_status_label = QLabel("Motion: None")
        self.recording_status_label = QLabel("Recording: Off")
        
        self.status_bar.addPermanentWidget(self.fps_label)
        self.status_bar.addPermanentWidget(self.motion_status_label)
        self.status_bar.addPermanentWidget(self.recording_status_label)
        
        # Initial camera refresh
        self.refresh_cameras()
    
    def connect_signals(self) -> None:
        """Connect signals and slots."""
        # Camera handler
        self.camera_handler.frame_ready.connect(self.update_frame)
        self.camera_handler.error_occurred.connect(self.show_error)
        self.camera_handler.fps_updated.connect(self.update_fps)
        
        # Motion detector
        self.motion_detector.motion_detected.connect(self.handle_motion_detected)
        
        # Video recorder
        self.video_recorder.recording_started.connect(self.on_recording_started)
        self.video_recorder.recording_stopped.connect(self.on_recording_stopped)
        self.video_recorder.recording_error.connect(self.show_error)
    
    def load_settings(self) -> None:
        """Load settings from configuration."""
        # Motion detection
        sensitivity = self.config.get('motion_sensitivity', 50)
        self.sensitivity_slider.setValue(sensitivity)
        self.motion_detector.set_sensitivity(sensitivity)
        
        motion_enabled = self.config.get('motion_detection_enabled', False)
        self.motion_check.setChecked(motion_enabled)
        
        # Recording mode
        recording_mode = self.config.get('recording_mode', 'continuous')
        if recording_mode == 'motion_triggered':
            self.recording_mode_combo.setCurrentText("Motion Triggered")
        else:
            self.recording_mode_combo.setCurrentText("Continuous")
        
        # Video recorder settings
        self.video_recorder.set_output_path(self.config.ensure_recording_path())
        self.video_recorder.set_recording_mode(recording_mode)
        self.video_recorder.set_motion_trigger_duration(
            self.config.get('motion_trigger_duration', 10)
        )
    
    def refresh_cameras(self) -> None:
        """Refresh the list of available cameras."""
        self.camera_combo.clear()
        cameras = CameraHandler.enumerate_cameras()
        
        if not cameras:
            self.camera_combo.addItem("No cameras found")
            self.start_btn.setEnabled(False)
            self.status_bar.showMessage("No cameras detected. Please connect a camera.", 5000)
        else:
            for index, name in cameras:
                self.camera_combo.addItem(name, index)
            self.start_btn.setEnabled(True)
            self.status_bar.showMessage(f"Found {len(cameras)} camera(s)", 3000)
    
    def toggle_viewing(self) -> None:
        """Toggle camera viewing on/off."""
        if not self.is_viewing:
            # Start viewing
            camera_index = self.camera_combo.currentData()
            if camera_index is None:
                self.show_error("Please select a valid camera")
                return
            
            if self.camera_handler.set_camera(camera_index):
                # Set camera properties from config
                width = self.config.get('resolution_width', 640)
                height = self.config.get('resolution_height', 480)
                self.camera_handler.set_resolution(width, height)
                self.camera_handler.set_fps(self.config.get('fps', 30))
                
                # Start camera thread
                self.camera_handler.start()
                self.is_viewing = True
                
                # Update UI
                self.start_btn.setText("Stop Viewing")
                self.camera_combo.setEnabled(False)
                self.refresh_cameras_btn.setEnabled(False)
                self.status_bar.showMessage("Camera started")
            else:
                self.show_error("Failed to start camera")
        else:
            # Stop viewing
            self.stop_viewing()
    
    def stop_viewing(self) -> None:
        """Stop camera viewing."""
        self.camera_handler.stop()
        self.is_viewing = False
        
        # Stop recording if active
        if self.video_recorder.is_recording_active():
            self.video_recorder.stop_recording()
        
        # Update UI
        self.start_btn.setText("Start Viewing")
        self.camera_combo.setEnabled(True)
        self.refresh_cameras_btn.setEnabled(True)
        self.video_label.clear()
        self.video_label.setText("Camera stopped")
        self.status_bar.showMessage("Camera stopped")
    
    @pyqtSlot(QImage, np.ndarray)
    def update_frame(self, qt_image: QImage, cv_frame: np.ndarray) -> None:
        """Update video display with new frame.
        
        Args:
            qt_image: QImage for display
            cv_frame: OpenCV frame for processing
        """
        try:
            self.current_frame = cv_frame
            
            # Process frame with motion detector if enabled
            if self.motion_detector.enabled:
                motion_detected, boxes, processed_frame = self.motion_detector.process_frame(cv_frame)
                
                # Convert processed frame back to QImage
                rgb_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888).copy()
                
                # Handle motion-triggered recording
                if self.video_recorder.recording_mode == 'motion_triggered':
                    self.video_recorder.handle_motion_detected(motion_detected, processed_frame)
            
            # Write frame to video if recording in continuous mode
            if self.video_recorder.is_recording_active() and self.video_recorder.recording_mode == 'continuous':
                self.video_recorder.write_frame(cv_frame)
            
            # Scale and display image
            pixmap = QPixmap.fromImage(qt_image)
            scaled_pixmap = pixmap.scaled(
                self.video_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.video_label.setPixmap(scaled_pixmap)
        except Exception as e:
            self.status_bar.showMessage(f"Frame processing error: {str(e)}", 3000)
    
    @pyqtSlot(float)
    def update_fps(self, fps: float) -> None:
        """Update FPS display.
        
        Args:
            fps: Current frames per second
        """
        self.fps_label.setText(f"FPS: {fps:.1f}")
    
    @pyqtSlot(bool, list)
    def handle_motion_detected(self, detected: bool, boxes: list) -> None:
        """Handle motion detection signal.
        
        Args:
            detected: True if motion detected
            boxes: List of bounding boxes
        """
        if detected:
            self.motion_status_label.setText(f"Motion: Detected ({len(boxes)} area(s))")
            self.motion_status_label.setStyleSheet("QLabel { color: red; font-weight: bold; }")
        else:
            self.motion_status_label.setText("Motion: None")
            self.motion_status_label.setStyleSheet("")
    
    def toggle_motion_detection(self, enabled: bool) -> None:
        """Toggle motion detection on/off.
        
        Args:
            enabled: True to enable, False to disable
        """
        self.motion_detector.set_enabled(enabled)
        self.config.set('motion_detection_enabled', enabled)
        self.config.save()
        
        if enabled:
            self.status_bar.showMessage("Motion detection enabled", 2000)
        else:
            self.status_bar.showMessage("Motion detection disabled", 2000)
            self.motion_status_label.setText("Motion: Disabled")
            self.motion_status_label.setStyleSheet("")
    
    def update_sensitivity(self, value: int) -> None:
        """Update motion detection sensitivity.
        
        Args:
            value: Sensitivity value (1-100)
        """
        self.sensitivity_label.setText(str(value))
        self.motion_detector.set_sensitivity(value)
        self.config.set('motion_sensitivity', value)
        self.config.save()
    
    def toggle_recording(self, enabled: bool) -> None:
        """Toggle recording on/off.
        
        Args:
            enabled: True to enable, False to disable
        """
        if enabled:
            if not self.is_viewing:
                self.recording_check.setChecked(False)
                self.show_error("Please start camera viewing before recording")
                return
            
            # Start recording
            if self.current_frame is not None:
                h, w = self.current_frame.shape[:2]
                if self.video_recorder.start_recording((w, h)):
                    self.status_bar.showMessage("Recording started", 2000)
                else:
                    self.recording_check.setChecked(False)
        else:
            # Stop recording
            self.video_recorder.stop_recording()
    
    def update_recording_mode(self, mode_text: str) -> None:
        """Update recording mode.
        
        Args:
            mode_text: Mode text ("Continuous" or "Motion Triggered")
        """
        mode = 'motion_triggered' if mode_text == "Motion Triggered" else 'continuous'
        self.video_recorder.set_recording_mode(mode)
        self.config.set('recording_mode', mode)
        self.config.save()
    
    @pyqtSlot(str)
    def on_recording_started(self, filename: str) -> None:
        """Handle recording started signal.
        
        Args:
            filename: Recording filename
        """
        self.recording_indicator.setStyleSheet("QLabel { color: red; font-size: 20px; }")
        self.recording_status_label.setText("Recording: Active")
        self.recording_status_label.setStyleSheet("QLabel { color: red; font-weight: bold; }")
    
    @pyqtSlot()
    def on_recording_stopped(self) -> None:
        """Handle recording stopped signal."""
        self.recording_indicator.setStyleSheet("QLabel { color: gray; font-size: 20px; }")
        self.recording_status_label.setText("Recording: Off")
        self.recording_status_label.setStyleSheet("")
        self.recording_check.setChecked(False)
    
    def show_settings(self) -> None:
        """Show settings dialog."""
        from ui.settings_dialog import SettingsDialog
        dialog = SettingsDialog(self.config, self)
        if dialog.exec():
            # Reload settings
            self.load_settings()
            self.status_bar.showMessage("Settings updated", 2000)
    
    def show_error(self, message: str) -> None:
        """Show error message.
        
        Args:
            message: Error message to display
        """
        # Show error in status bar
        self.status_bar.showMessage(f"Error: {message}", 5000)
        
        # For critical errors, show message box
        if "not available" in message.lower() or "disconnected" in message.lower():
            QMessageBox.critical(self, "Camera Error", message)
            # Stop viewing if camera error
            if self.is_viewing:
                self.stop_viewing()
    
    def closeEvent(self, event) -> None:
        """Handle window close event."""
        if self.is_viewing:
            self.stop_viewing()
        event.accept()


import cv2  # Import at end to avoid circular import issues

