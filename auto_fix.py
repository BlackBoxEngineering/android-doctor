#!/usr/bin/env python3
"""
Auto Fix - No button pressing required
Automatically attempts all recovery methods
"""

import subprocess
import time

def auto_fix():
    print("=== AUTO FIX - No Buttons Required ===")
    print("Attempting automatic recovery...")
    
    # Method 1: ADB network reset
    try:
        print("Trying ADB network reset...")
        subprocess.run(["adb", "shell", "svc", "wifi", "disable"], timeout=5)
        time.sleep(2)
        subprocess.run(["adb", "shell", "svc", "wifi", "enable"], timeout=5)
        subprocess.run(["adb", "shell", "svc", "data", "disable"], timeout=5)
        time.sleep(2)
        subprocess.run(["adb", "shell", "svc", "data", "enable"], timeout=5)
        print("Network reset completed")
    except:
        print("ADB method failed")
    
    # Method 2: Check if any device responds
    try:
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True, timeout=5)
        if "device" in result.stdout:
            print("Device found via ADB - attempting reboot")
            subprocess.run(["adb", "reboot"], timeout=10)
    except:
        pass
    
    # Method 3: Check fastboot
    try:
        result = subprocess.run(["fastboot", "devices"], capture_output=True, text=True, timeout=5)
        if result.stdout.strip():
            print("Device in fastboot - attempting reboot")
            subprocess.run(["fastboot", "reboot"], timeout=10)
    except:
        pass
    
    print("Auto fix complete. If still broken, phones are just terrible sometimes.")

if __name__ == "__main__":
    auto_fix()