@echo off
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

cd /d "%~dp0tools\SP_Flash_Tool"
if exist "flash_tool.exe" (
    start flash_tool.exe
) else (
    echo SP Flash Tool not found!
    echo Please download and extract SP Flash Tool to tools\SP_Flash_Tool\
    echo Download from: https://spflashtool.com/
)

echo.
echo Opening firmware folder...
start "" "%~dp0firmware\Nokia_G11"

echo.
echo Flash process ready. Follow the on-screen instructions.
pause
