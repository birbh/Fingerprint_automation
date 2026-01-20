# 🔍 Crime Lab Fingerprint Automation System

A complete forensic fingerprint identification system that automatically displays criminal dossiers when the Arduino fingerprint sensor detects a match.

## 🎯 System Overview

This system consists of four main components:

1. **Arduino Fingerprint Sensor** - Captures and matches fingerprints (returns FOUND_ID with confidence)
2. **Arduino GSR Sensor** - Measures galvanic skin response for stress detection (streams GSR_VAL every 500ms)
3. **Flask Web Server** - Displays criminal dossiers with real-time WebSocket updates and live GSR graph
4. **Python Serial Bridge** - Connects Arduino to web server, forwards fingerprint matches and GSR data

## 📋 Requirements

### Hardware
- Arduino Uno (or compatible)
- Adafruit Fingerprint Sensor (or compatible)
- GSR Sensor (Galvanic Skin Response / Lie Detector module, analog output on A0)
- USB cable to Arduino
- Jumper wires for sensor connections
- Mac/PC with USB ports

### Software
- Arduino IDE
- Python 3.8+
- MySQL Server
- Web browser

## 🚀 Installation

### Step 1: Install MySQL

**Option A: XAMPP (Recommended - Easier)**

1. Download XAMPP from [apachefriends.org](https://www.apachefriends.org/)
2. Install XAMPP
3. Open XAMPP Control Panel
4. Click "Start" for MySQL
5. Default settings:
   - Host: `localhost`
   - User: `root`
   - Password: (empty)
   - Port: `3306`

**Option B: Standalone MySQL (via Homebrew)**

```bash
# macOS
brew install mysql
brew services start mysql

# Secure your MySQL installation
mysql_secure_installation
```

### Step 2: Install Python Dependencies

```bash
# Navigate to project directory
cd /Users/bir_65/Fingerprint_automation

# Install required packages
pip3 install -r requirements.txt
```

### Step 3: Set Up Database

**Option A: Using phpMyAdmin (XAMPP users)**

1. Open browser: `http://localhost/phpmyadmin`
2. Click "SQL" tab at the top
3. Open `database/schema.sql` in a text editor
4. Copy all the SQL code
5. Paste into phpMyAdmin SQL window
6. Click "Go" button
7. You should see "crime_lab" database in the left sidebar

**Option B: Command Line**

```bash
# For XAMPP:
/Applications/XAMPP/xamppfiles/bin/mysql -u root
# (Press Enter - no password by default)

# For Homebrew MySQL:
mysql -u root -p

# Then run:
source database/schema.sql

# Or in one command:
mysql -u root -p < database/schema.sql

# Verify installation
mysql -u root -p -e "USE crime_lab; SHOW TABLES;"
```

### Step 4: Configure Database Password

Edit `web_app/app.py` and set your MySQL password:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # <-- Empty for XAMPP, or your password for Homebrew MySQL
    'database': 'crime_lab'
}
```

**Note:** XAMPP uses an empty password by default. If you set a password in XAMPP, update it here.

### Step 5: Prepare Suspect Images

1. Create mugshot images for your suspects
2. Place them in the `suspects_images/` folder
3. Name them: `suspect1.jpg`, `suspect2.jpg`, etc.
4. Match the ID numbers in your database

## 📱 Usage

### Phase 0: Wire Both Sensors

**Fingerprint Sensor:**
- BROWN wire → 5V
- ORANGE wire → GND
- BLUE wire → Pin 2
- WHITE wire → Pin 3

**GSR Sensor:**
- Signal pin → Arduino A0 (analog input)
- GND pin → Arduino GND
- VCC pin → Arduino 5V

### Phase 1: Enroll Suspects (One-Time Setup)

1. **Ensure Both Sensors are Wired (see Phase 0 above)**

2. **Wire the Fingerprint Sensor to Arduino:**

2. **Upload Enrollment Sketch:**
   ```bash
   # Open in Arduino IDE:
   arduino_sketches/fingerprint_enrollment/fingerprint_enrollment.ino
   
   # Upload to Arduino
   ```

3. **Enroll Fingerprints:**
   - Open Serial Monitor (Tools > Serial Monitor)
   - Set baud rate to 9600
   - Type `1` and press Enter for Suspect ID 1
   - Place finger on sensor twice
   - Repeat for IDs 2, 3, 4, 5, etc.

4. **Keep a Log:**
   ```
   ID 1 = John Doe (your thumb)
   ID 2 = Jane Smith (your index finger)
   ID 3 = Marcus Rodriguez (assistant's thumb)
   etc.
   ```

### Phase 2: Run the System

2. **Upload Identification Sketch (with GSR streaming):**
   ```bash
   # Open in Arduino IDE:
   arduino_sketches/fingerprint_identification/fingerprint_identification.ino
   # This sketch now streams both:
   #   - FOUND_ID:<id>:<confidence> (on fingerprint match)
   #   - GSR_VAL:<value> (every 500ms from A0 sensor)
   
   # Upload to Arduino
   # CLOSE the Serial Monitor after uploading!
   ```

2. **Start Flask Web Server:**
   ```bash
   cd web_app
   python3 app.py
   ```
   
   You should see:
   ```
   Crime Lab Web Server Starting...
   Access at: http://localhost:5000
   ```

3. **Find Your Arduino Port:**
   - Open Arduino IDE
   - Go to Tools > Port
   - Note the port name (e.g., `/dev/cu.usbmodem1101`)

4. **Configure Serial Listener:**
   Edit `serial_listener.py` and update the port:
   ```python
   ARDUINO_PORT = "/dev/cu.usbmodem1101"  # <-- Change this
   ```

5. **Start Serial Listener:**
   ```bash
   # In a new terminal window
   python3 serial_listener.py
   ```
   
   You should see:
   ```
   CRIME LAB - Serial Listener
   ✓ Connected to Arduino
   ✓ Flask server is running
   🔍 SYSTEM ACTIVE - Waiting for fingerprint matches...
   ```

### Phase 3: Demonstration

1. **Open the waiting page** (optional):
   ```
   http://localhost:5000
   ```

2. **Place a finger on the sensor**

3. **Watch the system in action:**
   - Arduino detects fingerprint match
   - Sends `FOUND_ID:<id>:<confidence>` signal
   - Python serial listener receives and logs to database
   - Browser automatically opens with criminal dossier
   - Meanwhile, Arduino streams `GSR_VAL:` readings every 500ms
   - Live GSR graph appears on dossier page in real-time
   - Graph auto-calibrates baseline from first 10 readings
   - Fingerprint confidence color-coded:
     - 🟢 GREEN: High confidence (200+/255)
     - 🟡 YELLOW: Medium confidence (150-199/255)
     - 🔴 RED: Low confidence (<150/255)
   - GSR graph color-coded for stress:
     - 🟢 GREEN: Stable (GSR < baseline × 1.3)
     - 🔴 RED: Stress detected (GSR > baseline × 1.3)
   - Graph shows last 50 data points, updates in real-time
   - Y-axis auto-scales for accurate visualization

## 🎨 Features

### Real-Time Updates
- WebSocket connection for instant dossier refresh
- Auto-navigation when new match detected
- Live system status indicator

### Criminal Dossier Display
- Mugshot with professional framing
- Full name and aliases
- Criminal charges
- Date of crime
- Complete arrest history
- Fingerprint match confidence score with color coding
- **LIVE GSR Polygraph Graph** (NEW):
  - Real-time stress detection visualization
  - Last 50 data points displayed
  - Auto-calibrated baseline (first 10 readings averaged)
  - Green/red stress indicator
  - Updates every 500ms from Arduino
  - Y-axis auto-scales for accuracy
- Timestamp of fingerprint match

### Database Tracking
- All suspects stored in MySQL `suspects` table
- Fingerprint match history in `match_history` table (with timestamps, confidence scores)
- GSR session data in `gsr_sessions` table (NEW):
  - Per-session baseline, peak, and readings stored as JSON
  - Timestamps for session start/end
  - Linked to suspect by ID
- Query interface for analysis and historical review

## 📁 Project Structure

```
Fingerprint_automation/
├── arduino_sketches/
│   ├── fingerprint_enrollment/
│   │   └── fingerprint_enrollment.ino
│   └── fingerprint_identification/
│       └── fingerprint_identification.ino
├── web_app/
│   ├── app.py
│   ├── templates/
│   │   ├── dossier.html
│   │   └── waiting.html
│   └── static/
├── suspects_images/
│   ├── suspect1.jpg
│   ├── suspect2.jpg
│   └── suspect3.jpg
├── database/
│   └── schema.sql
├── serial_listener.py
├── requirements.txt
└── README.md
```

## 🔧 Troubleshooting

### Arduino Not Connecting
```bash
# Check available ports
ls /dev/cu.*

# Try different baud rates (9600, 57600, 115200)
```

### Flask Server Not Starting
```bash
# Check if port 5000 is in use
lsof -i :5000

# Kill existing process
kill -9 <PID>
```

### Database Connection Error
```bash
# Verify MySQL is running
brew services list

# Test connection
mysql -u root -p -e "SHOW DATABASES;"

# Check password in app.py
```

### Mugshot Images Not Showing
- Verify images are in `suspects_images/` folder
- Check file names match database paths
- Ensure Flask static folder is configured
- Use relative paths in database: `suspects_images/suspect1.jpg`

### WebSocket Not Connecting
- Check browser console for errors
- Verify Flask-SocketIO is installed
- Try different browsers
- Check firewall settings

## 📊 Database Management

### View All Suspects
```bash
mysql -u root -p -e "USE crime_lab; SELECT id, name, charges FROM suspects;"
```

### View Match History
```bash
mysql -u root -p -e "USE crime_lab; SELECT s.name, mh.confidence_score, mh.matched_at FROM match_history mh JOIN suspects s ON mh.suspect_id = s.id ORDER BY mh.matched_at DESC;"
```

### Add New Suspect
```sql
INSERT INTO suspects (id, name, mugshot_path, charges, date_of_crime, aliases, arrest_history)
VALUES (6, 'New Suspect', 'suspects_images/suspect6.jpg', 'Charges here', '2024-01-01', 'Aliases', 'History');
```

### Clear Match History
```sql
DELETE FROM match_history;
```

## 🎓 Science Fair Tips

1. **Create Professional Mugshots:**
   - Use consistent lighting
   - Gray background
   - Front-facing photos
   - Add prisoner number overlay

2. **Prepare Demo Script:**
   - "This is a forensic fingerprint + polygraph detection system..."
   - Show enrollment process for both fingerprints
   - Explain GSR (galvanic skin response) and stress detection
   - Demonstrate real-time fingerprint matching with live graph
   - Explain confidence scoring and baseline calibration
   - Show how stress triggers color change in real-time

3. **Interactive Elements:**
   - Let judges place their finger (fingerprint match + GSR reading)
   - Show the database interface with match history
   - Explain WebSocket real-time updates and 500ms GSR streaming
   - Demonstrate multiple suspects with varying stress responses
   - Show graph auto-scaling and calibration

4. **Visual Aids:**
   - Print suspect dossiers with GSR graph examples
   - Show Arduino wiring diagram (both fingerprint + GSR sensors)
   - Display system architecture (Arduino → Serial → Flask → WebSocket → Browser)
   - Include fingerprint science facts + GSR/polygraph science
   - Explain baseline calculation (average of first 10 readings)
   - Show stress threshold formula (baseline × 1.3)

## 🔐 Security Notes

**This is a demonstration system for educational purposes.**

- Fingerprint data is stored on the sensor module
- Database contains sample/fake criminal records
- Not suitable for real security applications
- No encryption implemented
- Use only with consent of participants

## 📝 License

Educational project for science fair demonstration.

## 🤝 Credits

- Adafruit Fingerprint Sensor Library
- Flask and Flask-SocketIO
- MySQL Database
- Arduino Platform

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Verify all wiring connections
3. Confirm all dependencies are installed
4. Check that ports are correctly configured

---

**Good luck with your science fair! 🏆**
