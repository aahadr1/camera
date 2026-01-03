#!/usr/bin/env python3
"""
System check utility for Surveillance Camera Application.
Verifies dependencies, camera access, and system compatibility.
"""
import sys
import platform


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60)


def print_status(item, status, details=""):
    """Print a status line."""
    symbol = "✓" if status else "✗"
    print(f"{symbol} {item:<40} {details}")


def check_python_version():
    """Check Python version."""
    print_header("Python Environment")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    is_compatible = version.major == 3 and version.minor >= 8
    print_status("Python Version", is_compatible, version_str)
    
    if not is_compatible:
        print("  ⚠ Python 3.8 or higher is required")
    
    print_status("Platform", True, platform.platform())
    return is_compatible


def check_dependencies():
    """Check required packages."""
    print_header("Dependencies")
    
    all_installed = True
    
    # Check PyQt6
    try:
        import PyQt6.QtCore
        version = PyQt6.QtCore.PYQT_VERSION_STR
        print_status("PyQt6", True, f"v{version}")
    except ImportError:
        print_status("PyQt6", False, "Not installed")
        all_installed = False
    
    # Check OpenCV
    try:
        import cv2
        version = cv2.__version__
        print_status("opencv-python", True, f"v{version}")
    except ImportError:
        print_status("opencv-python", False, "Not installed")
        all_installed = False
    
    # Check NumPy
    try:
        import numpy
        version = numpy.__version__
        print_status("numpy", True, f"v{version}")
    except ImportError:
        print_status("numpy", False, "Not installed")
        all_installed = False
    
    return all_installed


def check_camera_access():
    """Check camera access."""
    print_header("Camera Access")
    
    try:
        import cv2
        
        # Try to detect cameras
        cameras_found = []
        for i in range(5):  # Check first 5 indices
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, _ = cap.read()
                if ret:
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    cameras_found.append((i, width, height))
                cap.release()
        
        if cameras_found:
            print_status("Camera Detection", True, f"Found {len(cameras_found)} camera(s)")
            for i, width, height in cameras_found:
                print(f"  Camera {i}: {width}x{height}")
        else:
            print_status("Camera Detection", False, "No cameras found")
            print("  ⚠ Please connect a USB camera and try again")
            return False
        
        return True
        
    except Exception as e:
        print_status("Camera Access", False, f"Error: {str(e)}")
        return False


def check_permissions():
    """Check file system permissions."""
    print_header("File System Permissions")
    
    from pathlib import Path
    import tempfile
    
    # Check home directory
    home_dir = Path.home()
    print_status("Home Directory", True, str(home_dir))
    
    # Check write permissions
    try:
        test_dir = home_dir / ".surveillance_camera"
        test_dir.mkdir(exist_ok=True)
        test_file = test_dir / ".write_test"
        test_file.touch()
        test_file.unlink()
        print_status("Config Directory", True, str(test_dir))
    except Exception as e:
        print_status("Config Directory", False, f"Cannot write: {str(e)}")
        return False
    
    # Check recording directory
    try:
        rec_dir = home_dir / "SurveillanceRecordings"
        rec_dir.mkdir(exist_ok=True)
        test_file = rec_dir / ".write_test"
        test_file.touch()
        test_file.unlink()
        print_status("Recording Directory", True, str(rec_dir))
    except Exception as e:
        print_status("Recording Directory", False, f"Cannot write: {str(e)}")
        return False
    
    return True


def check_display():
    """Check display availability."""
    print_header("Display Environment")
    
    if platform.system() == "Linux":
        import os
        display = os.environ.get("DISPLAY")
        if display:
            print_status("X Display", True, display)
            return True
        else:
            print_status("X Display", False, "DISPLAY not set")
            print("  ⚠ GUI applications may not work")
            return False
    else:
        print_status("Display", True, "Available")
        return True


def main():
    """Main check routine."""
    print("\n" + "=" * 60)
    print(" Surveillance Camera Application - System Check")
    print("=" * 60)
    
    results = {
        "Python Version": check_python_version(),
        "Dependencies": check_dependencies(),
        "Camera Access": check_camera_access(),
        "File Permissions": check_permissions(),
        "Display": check_display(),
    }
    
    print_header("Summary")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\nPassed: {passed}/{total} checks")
    
    if all(results.values()):
        print("\n✓ System is ready! You can run the application with:")
        print("  python3 run.py")
        print("  or")
        print("  python3 main.py")
        return 0
    else:
        print("\n✗ Some checks failed. Please fix the issues above.")
        
        if not results["Dependencies"]:
            print("\nTo install missing dependencies:")
            print("  pip install -r requirements.txt")
        
        if not results["Camera Access"]:
            print("\nCamera troubleshooting:")
            print("  - Ensure camera is connected")
            print("  - Check camera permissions")
            print("  - Close other apps using the camera")
        
        return 1


if __name__ == "__main__":
    sys.exit(main())

