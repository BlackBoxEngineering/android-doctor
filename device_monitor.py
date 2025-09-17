#!/usr/bin/env python3
"""
Real-time Device Monitor for Nokia G11
Continuously monitors USB connections and device state changes
"""

import time
import subprocess
import threading
from datetime import datetime
import winsound

class DeviceMonitor:
    def __init__(self):
        self.monitoring = False
        self.last_devices = set()
        self.detection_count = 0
        
    def get_current_devices(self):
        """Get currently connected USB devices"""
        try:
            result = subprocess.run([
                "powershell", "-Command",
                """Get-WmiObject -Class Win32_PnPEntity | Where-Object {
                    $_.Name -like '*MediaTek*' -or 
                    $_.Name -like '*Android*' -or 
                    $_.Name -like '*Nokia*' -or 
                    $_.Name -like '*MTK*' -or
                    $_.Name -like '*PreLoader*' -or
                    $_.Name -like '*Bootloader*' -or
                    $_.Name -like '*9008*' -or
                    $_.Name -like '*Qualcomm*'
                } | Select-Object Name, DeviceID"""
            ], capture_output=True, text=True, shell=True)
            
            devices = set()
            if result.stdout:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.strip() and not line.startswith('Name') and not line.startswith('----'):
                        devices.add(line.strip())
            
            return devices
        except Exception as e:
            print(f"Error getting devices: {e}")
            return set()
    
    def play_alert(self):
        """Play alert sound when device detected"""
        try:
            # Play system sound
            winsound.MessageBeep(winsound.MB_OK)
        except:
            print("\a")  # Fallback beep
    
    def log_detection(self, device_info, detection_type="DETECTED"):
        """Log device detection with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{'='*60}")
        print(f"[{timestamp}] DEVICE {detection_type}!")
        print(f"{'='*60}")
        print(device_info)
        print(f"{'='*60}")
        
        if detection_type == "DETECTED":
            self.detection_count += 1
            print(f"Detection #{self.detection_count}")
            self.play_alert()
            
            # Provide immediate action guidance
            if "MediaTek" in device_info or "PreLoader" in device_info:
                print("\n🚨 IMMEDIATE ACTION REQUIRED:")
                print("1. Open SP Flash Tool NOW!")
                print("2. Load scatter file")
                print("3. Click Download")
                print("4. Device may disappear in seconds!")
            elif "Android Bootloader" in device_info:
                print("\n🚨 FASTBOOT MODE DETECTED:")
                print("1. Open command prompt")
                print("2. Run: fastboot devices")
                print("3. Use fastboot commands for recovery")
    
    def monitor_continuously(self):
        """Continuously monitor for device changes"""
        print("🔍 Starting continuous device monitoring...")
        print("📱 Monitoring for Nokia G11 in recovery modes...")
        print("⚡ Try these while monitoring:")
        print("   • Hold Volume Down + plug USB")
        print("   • Hold Volume Up + plug USB")
        print("   • Let battery drain completely first")
        print("   • Try different USB ports/cables")
        print("\n💡 Press Ctrl+C to stop monitoring\n")
        
        self.monitoring = True
        self.last_devices = self.get_current_devices()
        
        try:
            while self.monitoring:
                current_devices = self.get_current_devices()
                
                # Check for new devices
                new_devices = current_devices - self.last_devices
                if new_devices:
                    for device in new_devices:
                        self.log_detection(device, "DETECTED")
                
                # Check for removed devices
                removed_devices = self.last_devices - current_devices
                if removed_devices:
                    for device in removed_devices:
                        self.log_detection(device, "DISCONNECTED")
                
                self.last_devices = current_devices
                
                # Show periodic status
                if int(time.time()) % 30 == 0:  # Every 30 seconds
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Monitoring... (Detections: {self.detection_count})")
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Monitoring stopped by user")
            self.monitoring = False
    
    def quick_scan(self):
        """Perform a quick device scan"""
        print("🔍 Quick device scan...")
        devices = self.get_current_devices()
        
        if devices:
            print("📱 Currently connected devices:")
            for device in devices:
                print(f"   • {device}")
                
            # Analyze device types
            for device in devices:
                if "MediaTek" in device or "PreLoader" in device:
                    print("\n✅ MediaTek PreLoader detected!")
                    print("   → Ready for SP Flash Tool")
                elif "Android Bootloader" in device:
                    print("\n✅ Android Bootloader detected!")
                    print("   → Ready for fastboot commands")
                elif "9008" in device or "Qualcomm" in device:
                    print("\n✅ Qualcomm EDL mode detected!")
                    print("   → Ready for QFIL tool")
        else:
            print("❌ No recovery-mode devices detected")
            print("💡 Try:")
            print("   • Hold Volume Down + connect USB")
            print("   • Hold Volume Up + connect USB")
            print("   • Let battery drain completely")
    
    def guided_detection(self):
        """Guide user through device detection process"""
        print("🎯 Guided Device Detection for Nokia G11")
        print("=" * 50)
        
        steps = [
            "Unplug your Nokia G11 from USB",
            "Hold Volume Down button",
            "While holding Volume Down, plug in USB cable",
            "Keep holding Volume Down for 5 seconds",
            "Release Volume Down button"
        ]
        
        for i, step in enumerate(steps, 1):
            print(f"\nStep {i}: {step}")
            if i < len(steps):
                input("Press Enter when ready for next step...")
            else:
                print("\nScanning for device...")
                time.sleep(2)
        
        # Check for device
        devices = self.get_current_devices()
        if devices:
            print("\n✅ Device detected!")
            for device in devices:
                print(f"   • {device}")
        else:
            print("\n❌ No device detected")
            print("\n🔄 Try alternative method:")
            print("1. Let battery drain completely")
            print("2. Try Volume Up instead of Volume Down")
            print("3. Try different USB cable/port")
            print("4. Run continuous monitoring")

def main():
    monitor = DeviceMonitor()
    
    print("📱 Nokia G11 Device Monitor")
    print("=" * 30)
    print("1. Quick Scan")
    print("2. Continuous Monitoring")
    print("3. Guided Detection")
    print("4. Exit")
    
    while True:
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            monitor.quick_scan()
        elif choice == '2':
            monitor.monitor_continuously()
        elif choice == '3':
            monitor.guided_detection()
        elif choice == '4':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    main()