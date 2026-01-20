# Quick Start Guide

## 🚀 Fast Setup (5 Minutes)

### 1. Install MySQL

**Using XAMPP (Easier):**
- Download & install XAMPP
- Open XAMPP Control Panel → Start MySQL
- Open `http://localhost/phpmyadmin`
- SQL tab → Paste contents of `database/schema.sql` → Go
- Verify `gsr_sessions` table is created (for polygraph data)

**Using Homebrew:**
```bash
brew install mysql
brew services start mysql
mysql -u root -p < database/schema.sql
# Verify: mysql -u root -p -e "USE crime_lab; SHOW TABLES;"
```

### 2. Install Python Packages
```bash
pip3 install -r requirements.txt
```

### 3. Configure
- Edit `web_app/app.py` → Set MySQL password (empty `''` for XAMPP)
- Edit `serial_listener.py` → Set Arduino port (check Arduino IDE > Tools > Port)

### 4. Add Suspect Images
- Place images in `suspects_images/` folder
- Name: `suspect1.jpg`, `suspect2.jpg`, etc.

### 5. Wire Sensors to Arduino

**Fingerprint Sensor:**
- BROWN → 5V
- ORANGE → GND
- BLUE → Pin 2
- WHITE → Pin 3

**GSR Sensor (Galvanic Skin Response / Polygraph):**
- Signal pin → Arduino A0 (analog input)
- GND pin → Arduino GND
- VCC pin → Arduino 5V

### 6. Enroll Fingerprints
```bash
# Upload: arduino_sketches/fingerprint_enrollment/fingerprint_enrollment.ino
# Open Serial Monitor, type ID numbers (1, 2, 3...)
# Scan each finger twice
```

### 7. Run System
```bash
# Terminal 1: Start web server
cd web_app
python3 app.py

# Terminal 2: Start serial listener (detects fingerprints + streams GSR)
python3 serial_listener.py

# Upload: arduino_sketches/fingerprint_identification/fingerprint_identification.ino
# Close Serial Monitor!
```

### 8. Test
- Place finger on sensor
- Browser opens automatically
- Dossier displays with fingerprint confidence score
- Live GSR graph updates in real-time with stress detection
- Graph auto-calibrates baseline from first 10 readings
- Red color = stress detected, Green = stable

---

## 📋 ID Mapping Log

Keep track of enrolled fingerprints:

```
ID 1: _____________________ (finger: _______)
ID 2: _____________________ (finger: _______)
ID 3: _____________________ (finger: _______)
ID 4: _____________________ (finger: _______)
ID 5: _____________________ (finger: _______)
```

---

## 🔧 Common Issues

**Port Error?**
```bash
ls /dev/cu.* # Find your Arduino port
```

**Database Error?**
```python
# In app.py, check:
DB_CONFIG = {'password': 'YOUR_PASSWORD'}
```

**Images Not Showing?**
- Files in `suspects_images/` folder?
- Named correctly (suspect1.jpg)?
- Database paths match?

---

See **SETUP_GUIDE.md** for detailed instructions.
