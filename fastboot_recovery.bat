@echo off
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
    if exist "firmware\Nokia_G11\recovery.img" (
        fastboot flash recovery "firmware\Nokia_G11\recovery.img"
    ) else (
        echo recovery.img not found in firmware folder
    )
)
if "%choice%"=="4" (
    if exist "firmware\Nokia_G11\boot.img" (
        fastboot flash boot "firmware\Nokia_G11\boot.img"
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
