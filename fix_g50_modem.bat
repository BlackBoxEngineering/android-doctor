@echo off
echo ========================================
echo Nokia G50 Modem Recovery - Method 2
echo ========================================
echo.
echo WARNING: This will flash modem firmware
echo Device must be in fastboot mode
echo.
echo Current status: Checking device...
fastboot devices
echo.
echo If device not shown above:
echo 1. Hold Volume Down + Power for 10 seconds
echo 2. Connect USB cable
echo 3. Device should show "FASTBOOT" on screen
echo.
echo Ready to flash modem? (Requires Nokia G50 firmware)
echo Download from: https://nokiafirmware.com/
echo.
echo Commands to run when firmware ready:
echo fastboot flash modem modem.img
echo fastboot flash radio radio.img
echo fastboot reboot
echo.
pause