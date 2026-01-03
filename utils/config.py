"""Configuration management for the surveillance application."""
import json
import os
from pathlib import Path
from typing import Any, Dict


class Config:
    """Manages application configuration and settings persistence."""
    
    DEFAULT_SETTINGS = {
        'motion_sensitivity': 50,
        'recording_path': str(Path.home() / 'SurveillanceRecordings'),
        'video_format': 'mp4',
        'video_codec': 'mp4v',
        'fps': 30,
        'resolution_width': 640,
        'resolution_height': 480,
        'motion_detection_enabled': False,
        'recording_mode': 'continuous',  # 'continuous' or 'motion_triggered'
        'motion_trigger_duration': 10,  # seconds to record after motion stops
        'last_camera_index': 0,
    }
    
    def __init__(self, config_file: str = None):
        """Initialize configuration manager.
        
        Args:
            config_file: Path to configuration file. Defaults to user's home directory.
        """
        if config_file is None:
            config_dir = Path.home() / '.surveillance_camera'
            config_dir.mkdir(exist_ok=True)
            config_file = config_dir / 'config.json'
        
        self.config_file = Path(config_file)
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.load()
    
    def load(self) -> None:
        """Load settings from configuration file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded_settings = json.load(f)
                    self.settings.update(loaded_settings)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config: {e}. Using defaults.")
    
    def save(self) -> None:
        """Save current settings to configuration file."""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except IOError as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key doesn't exist
            
        Returns:
            Configuration value or default
        """
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.
        
        Args:
            key: Configuration key
            value: Value to set
        """
        self.settings[key] = value
    
    def ensure_recording_path(self) -> str:
        """Ensure recording path exists and return it.
        
        Returns:
            Path to recording directory
        """
        path = Path(self.get('recording_path'))
        path.mkdir(parents=True, exist_ok=True)
        return str(path)

