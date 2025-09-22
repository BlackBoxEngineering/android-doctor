#!/usr/bin/env python3
"""
New Nokia G50 - Tesco SIM Calling Issues
Phone works but can't make outgoing calls
"""

import subprocess
import time

def fix_new_g50_calling():
    print("=== New Nokia G50 - Tesco SIM Calling Fix ===")
    print("SIM works but can't make outgoing calls")
    print("")
    
    # Reset network registration
    commands = [
        ["adb", "shell", "settings", "put", "global", "airplane_mode_on", "1"],
        ["adb", "shell", "am", "broadcast", "-a", "android.intent.action.AIRPLANE_MODE", "--ez", "state", "true"],
        ["adb", "shell", "settings", "put", "global", "airplane_mode_on", "0"],
        ["adb", "shell", "am", "broadcast", "-a", "android.intent.action.AIRPLANE_MODE", "--ez", "state", "false"],
        ["adb", "shell", "setprop", "ctl.restart", "ril-daemon"]
    ]
    
    print("Resetting network registration...")
    for cmd in commands:
        try:
            subprocess.run(cmd, timeout=5)
            time.sleep(2)
        except:
            print(f"Command failed: {' '.join(cmd[2:])}")
    
    print("\nManual fixes to try:")
    print("1. Settings > Network & Internet > Mobile Network")
    print("2. Turn off 'Enhanced 4G LTE Mode'")
    print("3. Change Network Mode to '3G only' temporarily")
    print("4. Settings > Apps > Phone > Storage > Clear Cache")
    print("5. Restart phone")
    print("")
    print("If still not working:")
    print("- Return phone as defective (it's new!)")
    print("- Try SIM in old phone to test if SIM is damaged")

if __name__ == "__main__":
    fix_new_g50_calling()