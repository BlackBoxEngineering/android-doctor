#!/usr/bin/env python3
"""
Emergency Recovery Tool for Nokia G11
Last resort recovery methods for severely bricked devices
"""

import os
import sys
import time
import subprocess
from pathlib import Path

class EmergencyRecovery:
    def __init__(self):
        self.working_dir = Path(__file__).parent
        
    def log(self, message):
        print(f"[EMERGENCY] {message}")
    
    def deep_flash_mode(self):
        """Attempt to enter deep flash mode"""
        self.log("=== DEEP FLASH MODE RECOVERY ===")
        self.log("This method works when normal PreLoader fails")
        self.log("")
        self.log("Steps:")
        self.log("1. Remove battery (if removable) for 30 seconds")
        self.log("2. Hold Volume Down + Volume Up + Power for 10 seconds")
        self.log("3. Release Power, keep holding Volume buttons")
        self.log("4. Connect USB cable while holding Volume buttons")
        self.log("5. Check Device Manager for 'MediaTek PreLoader'")
        self.log("")
        
        input("Press Enter when ready to check Device Manager...")
        
        # Check for device
        result = subprocess.run([
            "powershell", "-Command",
            "Get-WmiObject -Class Win32_PnPEntity | Where-Object {$_.Name -like '*MediaTek*' -or $_.Name -like '*PreLoader*'} | Select-Object Name"
        ], capture_output=True, text=True, shell=True)
        
        if "MediaTek" in result.stdout or "PreLoader" in result.stdout:
            self.log("SUCCESS! Device detected in deep flash mode")
            self.log("Now run SP Flash Tool immediately!")
            return True
        else:
            self.log("Device not detected. Try next method...")
            return False
    
    def test_point_method(self):
        """Guide for test point method (advanced)"""
        self.log("=== TEST POINT METHOD (ADVANCED) ===")
        self.log("WARNING: This requires opening the device!")
        self.log("")
        self.log("Nokia G11 Test Points (if accessible):")
        self.log("1. Power off device completely")
        self.log("2. Remove back cover (if possible)")
        self.log("3. Locate test points near CPU/flash chip")
        self.log("4. Short test points with tweezers")
        self.log("5. Connect USB while shorting")
        self.log("6. Device should appear as PreLoader")
        self.log("")
        self.log("CAUTION: This can permanently damage your device!")
        self.log("Only attempt if you have experience with hardware mods")
        
        response = input("Do you want to continue? (yes/no): ")
        return response.lower() == "yes"
    
    def battery_drain_recovery(self):
        """Complete battery drain method"""
        self.log("=== BATTERY DRAIN RECOVERY ===")
        self.log("Sometimes a completely dead battery helps reset the boot state")
        self.log("")
        self.log("Steps:")
        self.log("1. Let device boot loop until battery is completely dead")
        self.log("2. Leave it unplugged for 2-4 hours")
        self.log("3. Connect charger and immediately try recovery modes")
        self.log("4. Try Volume Down + Power while plugging USB")
        self.log("")
        
        self.log("Estimated time for complete drain: 2-6 hours")
        self.log("Monitor the device - when screen goes black, wait 2 more hours")
        
    def edl_mode_attempt(self):
        """Attempt Emergency Download Mode"""
        self.log("=== EDL MODE ATTEMPT ===")
        self.log("Emergency Download Mode (if supported)")
        self.log("")
        self.log("Try these key combinations:")
        self.log("1. Volume Up + Volume Down + Power (hold 15 seconds)")
        self.log("2. Volume Down + Power (hold 10 seconds, release Power, keep Volume Down)")
        self.log("3. Volume Up + Power (hold 10 seconds)")
        self.log("")
        
        for i in range(3):
            self.log(f"Attempt {i+1}/3 - Try key combination now...")
            time.sleep(10)
            
            # Check device manager
            result = subprocess.run([
                "powershell", "-Command",
                "Get-WmiObject -Class Win32_PnPEntity | Where-Object {$_.Name -like '*Qualcomm*' -or $_.Name -like '*9008*' -or $_.Name -like '*MediaTek*'} | Select-Object Name"
            ], capture_output=True, text=True, shell=True)
            
            if result.stdout.strip():
                self.log("Device detected!")
                self.log(result.stdout)
                return True
        
        return False
    
    def create_emergency_flash_script(self):
        """Create emergency flashing script"""
        script_path = self.working_dir / "emergency_flash.bat"
        
        script_content = """@echo off
echo ========================================
echo EMERGENCY FLASH - Nokia G11
echo ========================================
echo.
echo WARNING: This is for severely bricked devices only!
echo.
echo Prerequisites:
echo 1. SP Flash Tool installed
echo 2. MediaTek drivers installed  
echo 3. Nokia G11 firmware downloaded
echo 4. Device detected as PreLoader
echo.
echo EMERGENCY FLASH STEPS:
echo 1. Open SP Flash Tool
echo 2. Load scatter file
echo 3. Select "Format All + Download"
echo 4. Uncheck "Preloader" (if visible)
echo 5. Click "Format All"
echo 6. When prompted, connect device in PreLoader mode
echo.
echo This will COMPLETELY WIPE the device!
echo.
set /p confirm=Type EMERGENCY to continue: 
if not "%confirm%"=="EMERGENCY" (
    echo Cancelled.
    pause
    exit /b 1
)

echo.
echo Starting emergency flash process...
echo Connect device in PreLoader mode when prompted by SP Flash Tool
echo.

cd /d "%~dp0tools\\SP_Flash_Tool"
if exist "flash_tool.exe" (
    start flash_tool.exe
    echo SP Flash Tool started. Follow the emergency flash steps above.
) else (
    echo ERROR: SP Flash Tool not found!
    echo Please install SP Flash Tool first.
)

pause
"""
        
        with open(script_path, "w") as f:
            f.write(script_content)
        
        self.log("Emergency flash script created")
    
    def run_emergency_recovery(self):
        """Run all emergency recovery methods"""
        self.log("=== NOKIA G11 EMERGENCY RECOVERY ===")
        self.log("Use these methods when normal recovery fails")
        self.log("")
        
        methods = [
            ("Battery Drain Recovery", self.battery_drain_recovery),
            ("Deep Flash Mode", self.deep_flash_mode),
            ("EDL Mode Attempt", self.edl_mode_attempt),
            ("Test Point Method", self.test_point_method)
        ]
        
        for i, (name, method) in enumerate(methods, 1):
            self.log(f"Method {i}: {name}")
        
        self.log("")
        choice = input("Select method (1-4) or 'q' to quit: ")
        
        if choice == '1':
            self.battery_drain_recovery()
        elif choice == '2':
            self.deep_flash_mode()
        elif choice == '3':
            self.edl_mode_attempt()
        elif choice == '4':
            self.test_point_method()
        elif choice.lower() == 'q':
            return
        else:
            self.log("Invalid choice")
        
        # Create emergency script
        self.create_emergency_flash_script()

def main():
    recovery = EmergencyRecovery()
    recovery.run_emergency_recovery()

if __name__ == "__main__":
    main()