@echo off
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
