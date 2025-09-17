# Android Doctor - Nokia G11 Recovery System

A comprehensive recovery system for Nokia G11 devices stuck in boot loops or corrupted states.

## 🚨 Current Situation
Your Nokia G11 is in a USB boot loop with corruption message. The device is not being detected in Windows Device Manager, indicating it's not entering PreLoader mode during the boot cycle.

## 🛠️ Quick Start

### Method 1: Run Complete Recovery System
```bash
# Double-click to run
run_doctor.bat
```

### Method 2: Python Direct
```bash
python android_doctor.py
```

## 📋 Recovery Methods (In Order of Difficulty)

### 1. Battery Drain Method (RECOMMENDED FIRST)
- Let device boot loop until battery completely dies
- Leave unplugged for 2-4 hours  
- Try recovery modes when plugging back in

### 2. Real-time Device Monitoring
```bash
python device_monitor.py
```
- Monitors for brief PreLoader appearances
- Alerts when device is detected
- Guides immediate flashing action

### 3. Emergency Recovery Methods
```bash
python emergency_recovery.py
```
- Deep flash mode attempts
- EDL mode detection
- Advanced recovery techniques

## 🔧 Tools Included

### Core System (`android_doctor.py`)
- Automated device detection
- Driver installation guidance
- Firmware download assistance
- Recovery environment setup

### Device Monitor (`device_monitor.py`)
- Real-time USB monitoring
- Audio alerts for detection
- Guided detection process
- Quick device scanning

### Emergency Recovery (`emergency_recovery.py`)
- Battery drain recovery
- Deep flash mode
- Test point methods (advanced)
- Emergency flashing scripts

## 📁 Directory Structure
```
andriodDoctor/
├── android_doctor.py          # Main recovery system
├── device_monitor.py          # Real-time monitoring
├── emergency_recovery.py      # Emergency methods
├── run_doctor.bat            # Easy launcher
├── requirements.txt          # Dependencies
├── firmware/                 # Stock firmware storage
├── tools/                    # Recovery tools
└── logs/                     # System logs
```

## 🎯 Step-by-Step Recovery Process

### Phase 1: Preparation
1. Run `run_doctor.bat` to setup environment
2. Install MediaTek USB drivers (guided)
3. Download SP Flash Tool (guided)
4. Download Nokia G11 firmware (guided)

### Phase 2: Device Detection
1. Start device monitoring: `python device_monitor.py`
2. Try key combinations while monitoring:
   - Volume Down + USB connect
   - Volume Up + USB connect
   - Complete battery drain first

### Phase 3: Recovery Execution
**If PreLoader detected:**
- Run `flash_nokia_g11.bat`
- Use SP Flash Tool with scatter file
- Flash in "Download Only" mode

**If Fastboot detected:**
- Run `fastboot_recovery.bat`
- Use fastboot commands for recovery

**If nothing detected:**
- Run `python emergency_recovery.py`
- Try advanced recovery methods

## 🔍 Device Manager Detection Guide

Look for these in Device Manager:
- **Ports (COM & LPT)**: MediaTek PreLoader USB VCOM Port
- **Universal Serial Bus**: Unknown USB Device
- **Android Device**: Android Bootloader Interface

## ⚠️ Important Notes

### Current Status
- Device NOT detected in Device Manager
- No PreLoader or Fastboot mode visible
- Boot loop without USB handshake

### Critical Timing
- PreLoader mode may appear for only 2-3 seconds
- Must start flashing immediately when detected
- Use continuous monitoring for best results

### Recovery Success Indicators
- Device appears as "MediaTek PreLoader USB VCOM Port"
- SP Flash Tool can communicate with device
- Successful firmware flash completion

## 🆘 Emergency Contacts & Resources

### Firmware Sources
- [GetDroidTips Nokia G11](https://www.getdroidtips.com/nokia-g11-stock-firmware/)
- [Nokia Firmware](https://nokiafirmware.com/)
- [AndroidFileHost](https://www.androidfilehost.com/)

### Tool Downloads
- [SP Flash Tool](https://spflashtool.com/)
- [MediaTek USB Drivers](https://androidmtk.com/download-mediatek-usb-vcom-drivers)
- [ADB/Fastboot Tools](https://developer.android.com/studio/releases/platform-tools)

## 🔧 Troubleshooting

### Device Not Detected
1. Try different USB cables (data-capable)
2. Use USB 2.0 ports instead of USB 3.0
3. Install/reinstall MediaTek drivers
4. Let battery drain completely first

### SP Flash Tool Issues
1. Run as Administrator
2. Disable antivirus temporarily
3. Use "Download Only" mode
4. Ensure scatter file is correct

### Boot Loop Continues
1. Try emergency recovery methods
2. Consider hardware issues
3. Professional repair may be needed

## 📞 Support

For additional help:
1. Check logs in `logs/` folder
2. Run diagnostic: `python android_doctor.py diagnose`
3. Monitor continuously: `python device_monitor.py`

---

**Remember**: The key to Nokia G11 recovery is timing. The device may only be detectable for seconds during boot loop. Use continuous monitoring and be ready to flash immediately when detected.