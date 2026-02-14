# Quick Start Guide

## Fast Setup

### 1. Install MySQL

XAMPP (easy):
- Install XAMPP
- Start MySQL
- Open http://localhost/phpmyadmin
- Run database/schema.sql in the SQL tab

Homebrew:
```bash
brew install mysql
brew services start mysql
mysql -u root -p < database/schema.sql
```

### 2. Install Python Packages
```bash
pip3 install -r requirements.txt
```

### 3. Configure
- Set MySQL password in `web_app/app.py`
- Set Arduino port in `serial_listener.py`

### 4. Add Suspect Images
- Put images in `suspects_images/` as `suspect1.jpg`, `suspect2.jpg`, ...

### 5. Wire Sensors to Arduino

Fingerprint sensor:
- RED -> 5V
- GREEN -> GND
- YELLOW -> Pin 2
- BLACK -> Pin 3

GSR sensor:
- Signal -> A0
- GND -> GND
- VCC -> 5V

### 6. Enroll Fingerprints
```bash
# Upload: arduino_sketches/fingerprint_enrollment/fingerprint_enrollment.ino
# Open Serial Monitor, enter IDs, scan twice per ID
```

### 7. Run
```bash
# Terminal 1
cd web_app
python3 app.py

# Terminal 2
python3 serial_listener.py

# Upload: arduino_sketches/fingerprint_identification/fingerprint_identification.ino
```

### 8. Test
- Place a finger on the sensor
- Dossier opens in the browser
- GSR graph updates live


## 🔧 Common Issues

**Port Error?**
```bash
ls /dev/cu.* # Find your Arduino port
```

**Database Error?**
```python
# In app.py, check:
DB_CONFIG = {'password': 'YOUR_PASSWORD'}
(or leave blank to not use password)
```

**Images Not Showing?**
- Files in `suspects_images/` folder?
- Named correctly (suspect1.jpg)?
- Database paths match?

---

See **SETUP_GUIDE.md** for detailed instructions.
