"""Settings configuration dialog."""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSpinBox, QComboBox, QGroupBox, QFileDialog,
    QFormLayout, QDialogButtonBox
)
from PyQt6.QtCore import Qt
from pathlib import Path

from utils.config import Config


class SettingsDialog(QDialog):
    """Dialog for configuring application settings."""
    
    def __init__(self, config: Config, parent=None):
        """Initialize settings dialog.
        
        Args:
            config: Configuration manager
            parent: Parent widget
        """
        super().__init__(parent)
        self.config = config
        
        self.setWindowTitle("Settings")
        self.setMinimumWidth(500)
        
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self) -> None:
        """Setup the user interface."""
        layout = QVBoxLayout(self)
        
        # Camera settings
        camera_group = QGroupBox("Camera Settings")
        camera_layout = QFormLayout()
        
        self.fps_spin = QSpinBox()
        self.fps_spin.setMinimum(1)
        self.fps_spin.setMaximum(60)
        self.fps_spin.setValue(30)
        camera_layout.addRow("FPS:", self.fps_spin)
        
        # Resolution
        resolution_layout = QHBoxLayout()
        self.width_spin = QSpinBox()
        self.width_spin.setMinimum(320)
        self.width_spin.setMaximum(1920)
        self.width_spin.setSingleStep(160)
        self.width_spin.setValue(640)
        
        self.height_spin = QSpinBox()
        self.height_spin.setMinimum(240)
        self.height_spin.setMaximum(1080)
        self.height_spin.setSingleStep(120)
        self.height_spin.setValue(480)
        
        resolution_layout.addWidget(self.width_spin)
        resolution_layout.addWidget(QLabel("x"))
        resolution_layout.addWidget(self.height_spin)
        resolution_layout.addStretch()
        
        camera_layout.addRow("Resolution:", resolution_layout)
        
        camera_group.setLayout(camera_layout)
        layout.addWidget(camera_group)
        
        # Recording settings
        recording_group = QGroupBox("Recording Settings")
        recording_layout = QFormLayout()
        
        # Recording path
        path_layout = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_browse_btn = QPushButton("Browse...")
        self.path_browse_btn.clicked.connect(self.browse_path)
        path_layout.addWidget(self.path_edit, stretch=1)
        path_layout.addWidget(self.path_browse_btn)
        recording_layout.addRow("Save Path:", path_layout)
        
        # Video codec
        self.codec_combo = QComboBox()
        self.codec_combo.addItems([
            "mp4v - MPEG-4 (recommended)",
            "XVID - Xvid MPEG-4",
            "X264 - H.264",
            "MJPG - Motion JPEG"
        ])
        recording_layout.addRow("Video Codec:", self.codec_combo)
        
        # Motion trigger duration
        self.trigger_duration_spin = QSpinBox()
        self.trigger_duration_spin.setMinimum(1)
        self.trigger_duration_spin.setMaximum(60)
        self.trigger_duration_spin.setValue(10)
        self.trigger_duration_spin.setSuffix(" seconds")
        recording_layout.addRow("Motion Trigger Duration:", self.trigger_duration_spin)
        
        recording_group.setLayout(recording_layout)
        layout.addWidget(recording_group)
        
        # Motion detection settings
        motion_group = QGroupBox("Motion Detection Settings")
        motion_layout = QFormLayout()
        
        self.sensitivity_spin = QSpinBox()
        self.sensitivity_spin.setMinimum(1)
        self.sensitivity_spin.setMaximum(100)
        self.sensitivity_spin.setValue(50)
        motion_layout.addRow("Default Sensitivity:", self.sensitivity_spin)
        
        motion_group.setLayout(motion_layout)
        layout.addWidget(motion_group)
        
        # Dialog buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel |
            QDialogButtonBox.StandardButton.RestoreDefaults
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.StandardButton.RestoreDefaults).clicked.connect(
            self.restore_defaults
        )
        
        layout.addWidget(button_box)
    
    def load_settings(self) -> None:
        """Load settings from configuration."""
        self.fps_spin.setValue(self.config.get('fps', 30))
        self.width_spin.setValue(self.config.get('resolution_width', 640))
        self.height_spin.setValue(self.config.get('resolution_height', 480))
        self.path_edit.setText(self.config.get('recording_path', ''))
        
        # Codec
        codec = self.config.get('video_codec', 'mp4v')
        codec_map = {
            'mp4v': 0,
            'XVID': 1,
            'X264': 2,
            'MJPG': 3
        }
        self.codec_combo.setCurrentIndex(codec_map.get(codec, 0))
        
        self.trigger_duration_spin.setValue(self.config.get('motion_trigger_duration', 10))
        self.sensitivity_spin.setValue(self.config.get('motion_sensitivity', 50))
    
    def save_settings(self) -> None:
        """Save settings to configuration."""
        self.config.set('fps', self.fps_spin.value())
        self.config.set('resolution_width', self.width_spin.value())
        self.config.set('resolution_height', self.height_spin.value())
        self.config.set('recording_path', self.path_edit.text())
        
        # Codec
        codec_text = self.codec_combo.currentText()
        codec = codec_text.split(' - ')[0]
        self.config.set('video_codec', codec)
        
        self.config.set('motion_trigger_duration', self.trigger_duration_spin.value())
        self.config.set('motion_sensitivity', self.sensitivity_spin.value())
        
        self.config.save()
    
    def browse_path(self) -> None:
        """Browse for recording path."""
        path = QFileDialog.getExistingDirectory(
            self,
            "Select Recording Directory",
            self.path_edit.text() or str(Path.home())
        )
        if path:
            self.path_edit.setText(path)
    
    def restore_defaults(self) -> None:
        """Restore default settings."""
        defaults = Config.DEFAULT_SETTINGS
        self.fps_spin.setValue(defaults['fps'])
        self.width_spin.setValue(defaults['resolution_width'])
        self.height_spin.setValue(defaults['resolution_height'])
        self.path_edit.setText(defaults['recording_path'])
        self.codec_combo.setCurrentIndex(0)
        self.trigger_duration_spin.setValue(defaults['motion_trigger_duration'])
        self.sensitivity_spin.setValue(defaults['motion_sensitivity'])
    
    def accept(self) -> None:
        """Accept dialog and save settings."""
        self.save_settings()
        super().accept()

