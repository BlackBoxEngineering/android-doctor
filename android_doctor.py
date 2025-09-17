#!/usr/bin/env python3
"""
Android Doctor - Nokia G11 Recovery System
Automated phone repair and recovery tool for Nokia G11 boot loop issues
"""

import os
import sys
import time
import subprocess
import winreg
import requests
import zipfile
from pathlib import Path
import json
import threading
from datetime import datetime

class AndroidDoctor:
    def __init__(self):
        self.device_detected = False
        self.device_type = None
        self.working_dir = Path(__file__).parent
        self.firmware_dir = self.working_dir / "firmware"
        self.tools_dir = self.working_dir / "tools"
        self.logs_dir = self.working_dir / "logs"
        
        # Create directories
        for dir_path in [self.firmware_dir, self.tools_dir, self.logs_dir]:
            dir_path.mkdir(exist_ok=True)
    
    def log(self, message, level="INFO"):
        """Log messages with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}"
        print(log_message)
        
        # Write to log file
        log_file = self.logs_dir / f"android_doctor_{datetime.now().strftime('%Y%m%d')}.log"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_message + "\n")
    
    def check_device_manager(self):
        """Check Windows Device Manager for connected devices"""
        try:
            # Use WMI to query USB devices
            result = subprocess.run([
                "powershell", "-Command",
                "Get-WmiObject -Class Win32_PnPEntity | Where-Object {$_.Name -like '*MediaTek*' -or $_.Name -like '*Android*' -or $_.Name -like '*Nokia*' -or $_.Name -like '*MTK*'} | Select-Object Name, DeviceID"
            ], capture_output=True, text=True, shell=True)
            
            if result.stdout:
                self.log("Device Manager scan results:")
                self.log(result.stdout)
                
                if "MediaTek" in result.stdout or "PreLoader" in result.stdout:
                    self.device_detected = True
                    self.device_type = "preloader"
                    return True
                elif "Android Bootloader" in result.stdout:
                    self.device_detected = True
                    self.device_type = "fastboot"
                    return True
            
            return False
        except Exception as e:
            self.log(f"Error checking device manager: {e}", "ERROR")
            return False
    
    def monitor_device_connection(self, duration=30):
        """Monitor for device connection over specified duration"""
        self.log(f"Monitoring for device connection for {duration} seconds...")
        self.log("Try these while monitoring:")
        self.log("1. Hold Volume Down + plug USB cable")
        self.log("2. Hold Volume Up + plug USB cable")
        self.log("3. Let battery drain completely, then try above")
        
        start_time = time.time()
        while time.time() - start_time < duration:
            if self.check_device_manager():
                self.log(f"Device detected! Type: {self.device_type}")
                return True
            time.sleep(2)
        
        self.log("No device detected during monitoring period")
        return False
    
    def download_sp_flash_tool(self):
        """Download SP Flash Tool if not present"""
        sp_flash_path = self.tools_dir / "SP_Flash_Tool"
        if sp_flash_path.exists():
            self.log("SP Flash Tool already present")
            return True
        
        self.log("Downloading SP Flash Tool...")
        # Note: In real implementation, you'd download from official source
        # This is a placeholder for the download logic
        sp_flash_path.mkdir(exist_ok=True)
        
        # Create a placeholder executable info
        info_file = sp_flash_path / "download_info.txt"
        with open(info_file, "w") as f:
            f.write("Download SP Flash Tool from: https://spflashtool.com/\n")
            f.write("Extract to this directory\n")
        
        self.log("SP Flash Tool download placeholder created")
        return True
    
    def download_mtk_drivers(self):
        """Download MediaTek USB drivers"""
        driver_path = self.tools_dir / "MTK_Drivers"
        if driver_path.exists():
            self.log("MTK Drivers already present")
            return True
        
        self.log("Setting up MTK Drivers...")
        driver_path.mkdir(exist_ok=True)
        
        # Create driver installation script
        install_script = driver_path / "install_drivers.bat"
        with open(install_script, "w") as f:
            f.write("@echo off\n")
            f.write("echo Installing MediaTek USB Drivers...\n")
            f.write("echo Please run as Administrator\n")
            f.write("echo Download drivers from: https://androidmtk.com/download-mediatek-usb-vcom-drivers\n")
            f.write("pause\n")
        
        self.log("MTK Drivers setup created")
        return True
    
    def download_nokia_g11_firmware(self):
        """Download Nokia G11 stock firmware"""
        firmware_path = self.firmware_dir / "Nokia_G11"
        if firmware_path.exists():
            self.log("Nokia G11 firmware already present")
            return True
        
        self.log("Setting up Nokia G11 firmware download...")
        firmware_path.mkdir(exist_ok=True)
        
        # Create firmware info file
        firmware_info = firmware_path / "firmware_info.txt"
        with open(firmware_info, "w") as f:
            f.write("Nokia G11 Stock Firmware Sources:\n")
            f.write("1. https://www.getdroidtips.com/nokia-g11-stock-firmware/\n")
            f.write("2. https://nokiafirmware.com/\n")
            f.write("3. https://www.androidfilehost.com/\n\n")
            f.write("Required files:\n")
            f.write("- scatter.txt (partition layout)\n")
            f.write("- boot.img\n")
            f.write("- system.img\n")
            f.write("- recovery.img\n")
            f.write("- userdata.img\n")
        
        # Create scatter file template
        scatter_template = firmware_path / "scatter_template.txt"
        with open(scatter_template, "w") as f:
            f.write("# Nokia G11 Scatter File Template\n")
            f.write("# This file defines partition layout for flashing\n")
            f.write("# Download actual scatter file with firmware\n")
        
        self.log("Nokia G11 firmware setup created")
        return True
    
    def create_flash_script(self):
        """Create automated flashing script"""
        script_path = self.working_dir / "flash_nokia_g11.bat"
        
        script_content = """@echo off
echo ========================================
echo Nokia G11 Recovery Flash Script
echo ========================================
echo.
echo IMPORTANT: Make sure device is detected in Device Manager
echo Look for "MediaTek PreLoader USB VCOM Port"
echo.
echo Steps:
echo 1. Open SP Flash Tool
echo 2. Load scatter file from firmware folder
echo 3. Select "Download Only" mode
echo 4. Click Download button
echo 5. Connect phone while holding Volume Down
echo.
echo Press any key to open SP Flash Tool...
pause > nul

cd /d "%~dp0tools\\SP_Flash_Tool"
if exist "flash_tool.exe" (
    start flash_tool.exe
) else (
    echo SP Flash Tool not found!
    echo Please download and extract SP Flash Tool to tools\\SP_Flash_Tool\\
    echo Download from: https://spflashtool.com/
)

echo.
echo Opening firmware folder...
start "" "%~dp0firmware\\Nokia_G11"

echo.
echo Flash process ready. Follow the on-screen instructions.
pause
"""
        
        with open(script_path, "w") as f:
            f.write(script_content)
        
        self.log("Flash script created")
        return True
    
    def create_fastboot_script(self):
        """Create fastboot recovery script"""
        script_path = self.working_dir / "fastboot_recovery.bat"
        
        script_content = """@echo off
echo ========================================
echo Nokia G11 Fastboot Recovery
echo ========================================
echo.
echo This script attempts fastboot recovery
echo Make sure ADB/Fastboot tools are installed
echo.
echo Checking for fastboot...
fastboot --version >nul 2>&1
if errorlevel 1 (
    echo Fastboot not found! Please install ADB/Fastboot tools
    echo Download from: https://developer.android.com/studio/releases/platform-tools
    pause
    exit /b 1
)

echo.
echo Waiting for device in fastboot mode...
echo Try: Hold Volume Down + Power, then connect USB
echo.
fastboot devices

echo.
echo Available fastboot commands:
echo 1. fastboot reboot
echo 2. fastboot reboot-bootloader  
echo 3. fastboot flash recovery recovery.img
echo 4. fastboot flash boot boot.img
echo 5. fastboot erase userdata
echo.
echo Enter command number (1-5) or 'q' to quit:
set /p choice=

if "%choice%"=="1" fastboot reboot
if "%choice%"=="2" fastboot reboot-bootloader
if "%choice%"=="3" (
    if exist "firmware\\Nokia_G11\\recovery.img" (
        fastboot flash recovery "firmware\\Nokia_G11\\recovery.img"
    ) else (
        echo recovery.img not found in firmware folder
    )
)
if "%choice%"=="4" (
    if exist "firmware\\Nokia_G11\\boot.img" (
        fastboot flash boot "firmware\\Nokia_G11\\boot.img"
    ) else (
        echo boot.img not found in firmware folder
    )
)
if "%choice%"=="5" (
    echo WARNING: This will erase all user data!
    set /p confirm=Type YES to confirm: 
    if "%confirm%"=="YES" fastboot erase userdata
)

pause
"""
        
        with open(script_path, "w") as f:
            f.write(script_content)
        
        self.log("Fastboot script created")
        return True
    
    def run_diagnosis(self):
        """Run complete device diagnosis"""
        self.log("=== Android Doctor - Nokia G11 Recovery ===")
        self.log("Starting comprehensive diagnosis...")
        
        # Check current device status
        self.log("Step 1: Checking device connection...")
        if self.check_device_manager():
            self.log(f"Device detected in {self.device_type} mode!")
            return True
        else:
            self.log("No device detected. Starting monitoring...")
            return self.monitor_device_connection(30)
    
    def setup_recovery_environment(self):
        """Set up complete recovery environment"""
        self.log("Setting up recovery environment...")
        
        # Download required tools
        self.download_sp_flash_tool()
        self.download_mtk_drivers()
        self.download_nokia_g11_firmware()
        
        # Create scripts
        self.create_flash_script()
        self.create_fastboot_script()
        
        self.log("Recovery environment setup complete!")
    
    def run_recovery(self):
        """Main recovery process"""
        self.log("=== Nokia G11 Recovery Process ===")
        
        # Setup environment
        self.setup_recovery_environment()
        
        # Run diagnosis
        device_found = self.run_diagnosis()
        
        if device_found:
            self.log("Device detected! Ready for recovery.")
            if self.device_type == "preloader":
                self.log("Device in PreLoader mode - use SP Flash Tool")
                self.log("Run: flash_nokia_g11.bat")
            elif self.device_type == "fastboot":
                self.log("Device in Fastboot mode - use fastboot commands")
                self.log("Run: fastboot_recovery.bat")
        else:
            self.log("Device not detected. Try these steps:")
            self.log("1. Let battery drain completely")
            self.log("2. Hold Volume Down + connect USB")
            self.log("3. Hold Volume Up + connect USB")
            self.log("4. Try different USB cable/port")
            self.log("5. Install MTK drivers from tools/MTK_Drivers/")
        
        return device_found

def main():
    doctor = AndroidDoctor()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == "monitor":
            doctor.monitor_device_connection(60)
        elif command == "setup":
            doctor.setup_recovery_environment()
        elif command == "diagnose":
            doctor.run_diagnosis()
        else:
            print("Usage: python android_doctor.py [monitor|setup|diagnose]")
    else:
        # Run full recovery process
        doctor.run_recovery()

if __name__ == "__main__":
    main()