#!/usr/bin/env python3
"""
Quick Device Monitor for Nokia G11 - Windows Compatible
"""

import time
import subprocess
from datetime import datetime

def get_devices():
    """Get MediaTek/Android devices"""
    try:
        result = subprocess.run([
            "powershell", "-Command",
            "Get-WmiObject -Class Win32_PnPEntity | Where-Object {$_.Name -like '*MediaTek*' -or $_.Name -like '*Android*' -or $_.Name -like '*Nokia*' -or $_.Name -like '*MTK*' -or $_.Name -like '*PreLoader*'} | Select-Object Name"
        ], capture_output=True, text=True, shell=True)
        
        if result.stdout and "MediaTek" in result.stdout:
            return result.stdout.strip()
        return None
    except:
        return None

def monitor_device():
    """Monitor for Nokia G11 recovery modes"""
    print("=== Nokia G11 Device Monitor ===")
    print("Monitoring for device in recovery mode...")
    print("Try these while monitoring:")
    print("1. Hold Volume Down + plug USB")
    print("2. Hold Volume Up + plug USB") 
    print("3. Let battery drain completely first")
    print("\nPress Ctrl+C to stop\n")
    
    detection_count = 0
    
    try:
        while True:
            devices = get_devices()
            if devices:
                detection_count += 1
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"\n[{timestamp}] DEVICE DETECTED #{detection_count}!")
                print("=" * 50)
                print(devices)
                print("=" * 50)
                
                if "MediaTek" in devices or "PreLoader" in devices:
                    print("PRELOADER MODE DETECTED!")
                    print("1. Open SP Flash Tool NOW!")
                    print("2. Load scatter file")
                    print("3. Click Download")
                    print("4. Device may disappear in seconds!")
                elif "Android" in devices:
                    print("ANDROID BOOTLOADER DETECTED!")
                    print("1. Open command prompt")
                    print("2. Run: fastboot devices")
                
                # Alert sound
                print("\a")  # System beep
            
            # Status update every 30 seconds
            if int(time.time()) % 30 == 0:
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"[{timestamp}] Monitoring... (Detections: {detection_count})")
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\nMonitoring stopped. Total detections: {detection_count}")

if __name__ == "__main__":
    monitor_device()