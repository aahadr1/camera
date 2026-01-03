#!/usr/bin/env python3
"""
Convenience script to run the surveillance camera application.
This script checks for dependencies and provides helpful error messages.
"""
import sys
import subprocess


def check_dependencies():
    """Check if required packages are installed."""
    required_packages = ['PyQt6', 'cv2', 'numpy']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'cv2':
                import cv2
            elif package == 'PyQt6':
                import PyQt6
            elif package == 'numpy':
                import numpy
        except ImportError:
            if package == 'cv2':
                missing_packages.append('opencv-python')
            else:
                missing_packages.append(package)
    
    return missing_packages


def main():
    """Main entry point."""
    print("=" * 60)
    print("Surveillance Camera Application")
    print("=" * 60)
    print()
    
    # Check dependencies
    print("Checking dependencies...")
    missing = check_dependencies()
    
    if missing:
        print("\n❌ Missing required packages:")
        for package in missing:
            print(f"   - {package}")
        print("\nPlease install missing packages using:")
        print("   pip install -r requirements.txt")
        print()
        return 1
    
    print("✓ All dependencies are installed")
    print()
    print("Starting application...")
    print()
    
    # Run the application
    from main import main as app_main
    app_main()


if __name__ == '__main__':
    sys.exit(main())

