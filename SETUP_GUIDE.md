# Crime Lab Fingerprint Automation System

Fingerprint identification with a web UI and optional GSR sensor input.

## System Overview

- Arduino fingerprint sensor sends FOUND_ID and confidence
- Arduino GSR sensor streams GSR_VAL every 500ms
- Flask app serves the dossier UI and live graph
- Python serial listener bridges Arduino to Flask

## Requirements

Hardware:
- Arduino Uno (or other compatible device)
- Fingerprint sensor (Adafruit-compatible or similar)
- GSR sensor (analog out to A0)
- USB cable and jumper wires

Software:
- Arduino IDE
- Python 3.8+
- MySQL Server
- Web browser

## 🚀 Installation

### Step 1: Install MySQL

Option A: XAMPP (easy)

1. Download XAMPP from [apachefriends.org](https://www.apachefriends.org/)
2. Install XAMPP
3. Open XAMPP Control Panel
4. Click "Start" for MySQL
5. Default settings:
   - Host: `localhost`
   - User: `root`
   - Password: (empty)
   - Port: `3306`

Option B: Homebrew

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

Option A: phpMyAdmin

1. Open browser: `http://localhost/phpmyadmin`
2. Click "SQL" tab at the top
3. Open `database/schema.sql` in a text editor
4. Copy all the SQL code
5. Paste into phpMyAdmin SQL window
6. Click "Go" button
7. You should see "crime_lab" database in the left sidebar

Option B: Command line

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
    'password': '',  # leave empty for no pass.
    'database': 'crime_lab'
}
```

Note: XAMPP uses an empty password by default.

### Step 5: Prepare Suspect Images

1. Create mugshot images for your suspects
2. Place them in the `suspects_images/` folder
3. Name them: `suspect1.jpg`, `suspect2.jpg`, etc.
4. Match the ID numbers in your database

## Usage

### Phase 0: Wire Both Sensors

Fingerprint sensor:
- RED -> 5V
- GREEN -> GND
- YELLOW -> Pin 2
- BLACK -> Pin 3

GSR sensor:
- Signal -> A0
- GND -> GND
- VCC -> 5V

### Phase 1: Enroll Suspects (One-Time Setup)

1. Ensure both sensors are wired.
2. Upload enrollment sketch:
   ```bash
   # Open in Arduino IDE:
   arduino_sketches/fingerprint_enrollment/fingerprint_enrollment.ino
   
   # Upload to Arduino
   ```

3. Enroll fingerprints:
   - Open Serial Monitor (Tools > Serial Monitor)
   - Set baud rate to 9600
   - Type `1` and press Enter for Suspect ID 1
   - Place finger on sensor twice
   - Repeat for IDs 2, 3, 4, 5, etc.

4. Keep a log:
   ```
   ID 1 = name1 (your thumb)
   ID 2 = name2 (your index finger)
   etc.
   ```

### Phase 2: Run the System

1. Upload identification sketch (with GSR streaming):
   ```bash
   # Open in Arduino IDE:
   arduino_sketches/fingerprint_identification/fingerprint_identification.ino
   # This sketch now streams both:
   #   - FOUND_ID:<id>:<confidence> (on fingerprint match)
   #   - GSR_VAL:<value> (every 500ms from A0 sensor)
   
   # Upload to Arduino
   # CLOSE the Serial Monitor after uploading!
   ```

2. Start Flask Web Server:
   ```bash
   cd web_app
   python3 app.py
   ```
   
   You should see:
   ```
   Crime Lab Web Server Starting...
   Access at: http://localhost:5000
   ```

3. Find your Arduino port:
   - Open Arduino IDE
   - Go to Tools > Port
   - Note the port name (e.g., `/dev/cu.usbmodem1101`)

4. Configure serial listener:
   Edit `serial_listener.py` and update the port:
   ```python
   ARDUINO_PORT = "/dev/cu.usbmodem1101"  # <-- Change this
   ```

5. Start serial listener:
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

1. Open the waiting page (optional):
   ```
   http://localhost:5000
   ```

2. **Place a finger on the sensor**

3. Watch the system in action:
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

## Features

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

## Database Management

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

## Notes

- Fingerprint wire colors may vary by sensor model.
- GSR readings are sensitive to contact quality.
