#!/usr/bin/env python3
"""
Surveillance Camera Application
Main entry point for the application.
"""
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from ui.main_window import MainWindow
from utils.config import Config


def main():
    """Main application entry point."""
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Surveillance Camera")
    app.setOrganizationName("SurveillanceApp")
    
    # Load configuration
    config = Config()
    
    # Create and show main window
    window = MainWindow(config)
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

