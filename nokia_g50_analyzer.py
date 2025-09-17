#!/usr/bin/env python3
"""
Nokia G50 SIM/Network Analyzer
Diagnoses and fixes SIM connectivity issues after physical damage
"""

import subprocess
import time
from datetime import datetime

class NokiaG50Analyzer:
    def __init__(self):
        self.device_connected = False
        self.adb_available = False
        
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def check_adb_connection(self):
        """Check if G50 is connected via ADB"""
        try:
            result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
            if "device" in result.stdout and not "List of devices" in result.stdout.replace("List of devices attached", ""):
                self.device_connected = True
                self.adb_available = True
                return True
        except:
            pass
        return False
    
    def check_fastboot_connection(self):
        """Check if G50 is in fastboot mode"""
        try:
            result = subprocess.run(["fastboot", "devices"], capture_output=True, text=True)
            if result.stdout.strip():
                self.device_connected = True
                return True
        except:
            pass
        return False
    
    def get_device_info(self):
        """Get device information via ADB"""
        if not self.adb_available:
            return None
        
        info = {}
        commands = {
            "model": "getprop ro.product.model",
            "baseband": "getprop ro.baseband",
            "radio": "getprop ro.radio.version", 
            "imei": "service call iphonesubinfo 1",
            "sim_state": "getprop gsm.sim.state",
            "network_type": "getprop gsm.network.type"
        }
        
        for key, cmd in commands.items():
            try:
                result = subprocess.run(["adb", "shell", cmd], capture_output=True, text=True)
                info[key] = result.stdout.strip()
            except:
                info[key] = "Unknown"
        
        return info
    
    def check_sim_hardware(self):
        """Check SIM card hardware status"""
        self.log("=== SIM Hardware Diagnosis ===")
        
        if not self.adb_available:
            self.log("ADB not available - enable USB debugging first")
            return False
        
        # Check SIM detection
        try:
            result = subprocess.run(["adb", "shell", "getprop", "gsm.sim.state"], capture_output=True, text=True)
            sim_state = result.stdout.strip()
            
            self.log(f"SIM State: {sim_state}")
            
            if "ABSENT" in sim_state:
                self.log("SIM card not detected - possible hardware damage")
                return False
            elif "READY" in sim_state:
                self.log("SIM card detected and ready")
                return True
            else:
                self.log(f"SIM in unknown state: {sim_state}")
                return False
                
        except Exception as e:
            self.log(f"Error checking SIM: {e}")
            return False
    
    def check_baseband_modem(self):
        """Check baseband/modem status"""
        self.log("=== Baseband/Modem Diagnosis ===")
        
        if not self.adb_available:
            return False
        
        try:
            # Check baseband version
            result = subprocess.run(["adb", "shell", "getprop", "ro.baseband"], capture_output=True, text=True)
            baseband = result.stdout.strip()
            self.log(f"Baseband Version: {baseband}")
            
            if not baseband or baseband == "unknown":
                self.log("WARNING: Baseband not detected - modem may be corrupted")
                return False
            
            # Check radio interface
            result = subprocess.run(["adb", "shell", "getprop", "ril.version"], capture_output=True, text=True)
            ril = result.stdout.strip()
            self.log(f"RIL Version: {ril}")
            
            return True
            
        except Exception as e:
            self.log(f"Error checking baseband: {e}")
            return False
    
    def run_network_diagnostics(self):
        """Run comprehensive network diagnostics"""
        self.log("=== Network Diagnostics ===")
        
        if not self.adb_available:
            return
        
        diagnostics = [
            ("Network Operator", "getprop gsm.operator.alpha"),
            ("Network Type", "getprop gsm.network.type"),
            ("Signal Strength", "dumpsys telephony.registry | grep mSignalStrength"),
            ("Data Connection", "getprop gsm.data.state"),
            ("Radio Power", "getprop gsm.radio.power")
        ]
        
        for name, cmd in diagnostics:
            try:
                result = subprocess.run(["adb", "shell"] + cmd.split(), capture_output=True, text=True)
                value = result.stdout.strip()
                self.log(f"{name}: {value}")
            except:
                self.log(f"{name}: Unable to retrieve")
    
    def create_g50_recovery_script(self):
        """Create Nokia G50 specific recovery script"""
        script_content = """@echo off
echo ========================================
echo Nokia G50 SIM/Network Recovery
echo ========================================
echo.
echo This script attempts to fix SIM connectivity issues
echo.
echo Prerequisites:
echo 1. Enable USB Debugging (Developer Options)
echo 2. Install ADB drivers
echo 3. Device connected and recognized
echo.
echo Recovery Methods:
echo 1. Reset Network Settings
echo 2. Flash Modem/Baseband
echo 3. Factory Reset (last resort)
echo.
set /p choice=Select method (1-3): 

if "%choice%"=="1" (
    echo Resetting network settings...
    adb shell settings put global airplane_mode_on 1
    timeout /t 3 /nobreak >nul
    adb shell settings put global airplane_mode_on 0
    adb shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false
    echo Network reset complete
)

if "%choice%"=="2" (
    echo WARNING: Flashing modem requires bootloader unlock
    echo This will void warranty and may brick device
    set /p confirm=Type YES to continue: 
    if "%confirm%"=="YES" (
        echo Rebooting to fastboot...
        adb reboot bootloader
        echo Flash modem.img from Nokia G50 firmware
        echo fastboot flash modem modem.img
    )
)

if "%choice%"=="3" (
    echo WARNING: This will erase all data!
    set /p confirm=Type FACTORY to continue: 
    if "%confirm%"=="FACTORY" (
        adb shell recovery --wipe_data
    )
)

pause
"""
        
        with open("nokia_g50_recovery.bat", "w") as f:
            f.write(script_content)
        
        self.log("Nokia G50 recovery script created")
    
    def analyze_g50(self):
        """Main analysis function for Nokia G50"""
        self.log("=== Nokia G50 SIM/Network Analyzer ===")
        self.log("Analyzing dropped Nokia G50 with SIM connectivity issues...")
        
        # Check connections
        self.log("Checking device connection...")
        
        if self.check_adb_connection():
            self.log("Device connected via ADB")
            
            # Get device info
            info = self.get_device_info()
            if info:
                self.log("=== Device Information ===")
                for key, value in info.items():
                    self.log(f"{key.upper()}: {value}")
            
            # Run diagnostics
            sim_ok = self.check_sim_hardware()
            baseband_ok = self.check_baseband_modem()
            self.run_network_diagnostics()
            
            # Provide recommendations
            self.log("=== Recommendations ===")
            if not sim_ok:
                self.log("1. Check SIM card physically - may be damaged")
                self.log("2. Try SIM in another phone")
                self.log("3. Clean SIM contacts")
            
            if not baseband_ok:
                self.log("1. Modem/baseband corruption detected")
                self.log("2. May need firmware reflash")
                self.log("3. Consider professional repair")
            
            if sim_ok and baseband_ok:
                self.log("1. Try network reset first")
                self.log("2. Check with carrier")
                self.log("3. Software issue likely")
                
        elif self.check_fastboot_connection():
            self.log("Device in fastboot mode - ready for firmware flash")
            
        else:
            self.log("Device not detected")
            self.log("Enable USB debugging or enter fastboot mode")
        
        # Create recovery script
        self.create_g50_recovery_script()

def main():
    analyzer = NokiaG50Analyzer()
    analyzer.analyze_g50()

if __name__ == "__main__":
    main()