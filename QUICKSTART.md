# Quick Reference Card

## 🚀 Quick Start (3 Steps)

### 1️⃣ Hardware
```
Sensor → Arduino:
VCC → 5V
GND → GND  
TX → Pin 2
RX → Pin 3
```

### 2️⃣ Upload
- Open `arduino_fingerprint.ino` in Arduino IDE
- Install "Adafruit Fingerprint" library
- Upload to Arduino

### 3️⃣ Run
```bash
cd python_backend
pip3 install -r requirements.txt
python3 fingerprint_app.py -p /dev/ttyUSB0  # Linux
python fingerprint_app.py -p COM3           # Windows
```

---

## 📝 Common Commands

| Command | Action | Example |
|---------|--------|---------|
| `enroll <ID>` | Add new fingerprint | `enroll 1` |
| `scan` or `s` | Match fingerprint | `scan` |
| `add <ID>` | Add suspect data | `add 1` |
| `list` or `l` | Show all suspects | `list` |
| `count` or `c` | Show total stored | `count` |
| `delete <ID>` | Remove fingerprint | `delete 1` |
| `help` or `h` | Show help | `help` |
| `quit` or `q` | Exit program | `quit` |

---

## 🔄 Typical Workflow

```
1. START
   └─► python3 fingerprint_app.py -p /dev/ttyUSB0

2. ENROLL
   ├─► Type: enroll 1
   ├─► Place finger (twice)
   └─► Enter: Name, Age, Description, Photo path

3. SCAN
   ├─► Type: scan
   ├─► Place finger
   └─► View: Suspect info + photo (auto-opens)

4. MANAGE
   ├─► list  - View all suspects
   ├─► count - Check total stored
   └─► delete 1 - Remove suspect
```

---

## ⚠️ Troubleshooting Quick Fix

| Problem | Quick Fix |
|---------|-----------|
| Sensor not found | Check VCC/GND, verify TX/RX crossed |
| Can't connect | Close Arduino Serial Monitor first |
| No match | Clean sensor, dry finger, try again |
| Python error | Install: `pip3 install pyserial` |
| Permission error (Linux) | `sudo usermod -a -G dialout $USER` |

---

## 📍 Important Paths

- **Arduino Code**: `arduino_fingerprint/arduino_fingerprint.ino`
- **Python App**: `python_backend/fingerprint_app.py`
- **Database**: `python_backend/suspects_database.json` (auto-created)
- **Images**: `suspect_images/` (store photos here)
- **Full Guide**: `docs/GUIDE.md`

---

## 💡 Pro Tips

✅ Keep sensor clean for best results
✅ Use fingerprint center, not tip
✅ Backup `suspects_database.json` regularly
✅ Store images in `suspect_images/` folder
✅ Use descriptive suspect IDs (1-127)

---

## 🆘 Get Help

- Full documentation: `docs/GUIDE.md`
- Troubleshooting: `docs/GUIDE.md#troubleshooting`
- Command help: Type `help` in app
- Hardware guide: `docs/GUIDE.md#hardware-setup`

---

**For detailed instructions, see [docs/GUIDE.md](docs/GUIDE.md)**
