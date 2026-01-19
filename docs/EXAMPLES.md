# Example Usage Scenarios

## Scenario 1: First Time Setup

### Step 1: Install and Start
```bash
# Install requirements
cd python_backend
pip3 install -r requirements.txt

# Start the application
python3 fingerprint_app.py -p /dev/ttyUSB0
```

**Output:**
```
============================================================
🔐 FINGERPRINT AUTOMATION SYSTEM
============================================================
✓ Connected to Arduino on /dev/ttyUSB0
  Arduino: Fingerprint Automation System
  Arduino: ==============================
  Arduino: READY:Fingerprint sensor found!

📖 AVAILABLE COMMANDS:
  scan (s)         - Scan fingerprint and display suspect info
  enroll <ID> (e)  - Enroll new fingerprint with ID
  add <ID>         - Add/update suspect information for ID
  list (l)         - List all suspects in database
  count (c)        - Show number of stored fingerprints
  delete <ID> (d)  - Delete fingerprint and suspect data
  help (h)         - Show this help message
  quit (q)         - Exit application

>
```

### Step 2: Enroll First Fingerprint
```bash
> enroll 1
```

**Output:**
```
📝 Enrolling fingerprint ID: 1
Follow the instructions from Arduino...
  Arduino: ENROLL_START:1
  Arduino: STATUS:Place finger on sensor...
[User places finger]
  Arduino: STATUS:Image taken
  Arduino: STATUS:Image converted
  Arduino: STATUS:Remove finger
[User removes finger]
  Arduino: STATUS:Place same finger again...
[User places same finger]
  Arduino: STATUS:Image taken
  Arduino: STATUS:Image converted
  Arduino: STATUS:Creating model...
  Arduino: STATUS:Prints matched!
  Arduino: STATUS:Storing model #1
  Arduino: ENROLL_SUCCESS:1

📝 Enter suspect information:
  Name: John Doe
  Age: 35
  Description: Robbery suspect, case #2024-001
  Image path (optional, press Enter to skip): /home/user/suspects/john_doe.jpg

✓ Added suspect: John Doe (ID: 1)
✓ Database saved (1 suspects)

>
```

### Step 3: Enroll More Suspects
```bash
> enroll 2
```

**Output:**
```
📝 Enrolling fingerprint ID: 2
Follow the instructions from Arduino...
  [Enrollment process...]
  
📝 Enter suspect information:
  Name: Jane Smith
  Age: 28
  Description: Fraud case #2024-015
  Image path (optional, press Enter to skip): /home/user/suspects/jane_smith.jpg

✓ Added suspect: Jane Smith (ID: 2)
✓ Database saved (2 suspects)

>
```

---

## Scenario 2: Daily Operations

### Check How Many Fingerprints Are Stored
```bash
> count
```

**Output:**
```
  Arduino: COUNT:2

📊 Fingerprints stored: 2

>
```

### List All Suspects
```bash
> list
```

**Output:**
```
============================================================
📋 SUSPECTS DATABASE
============================================================

ID 1:
  Name:        John Doe
  Age:         35
  Description: Robbery suspect, case #2024-001
  Registered:  2024-01-15T10:30:00

ID 2:
  Name:        Jane Smith
  Age:         28
  Description: Fraud case #2024-015
  Registered:  2024-01-15T11:45:00
============================================================

>
```

### Scan Unknown Fingerprint (Match Found)
```bash
> scan
```

**Output:**
```
🔍 Scanning fingerprint...
Place finger on sensor...
  Arduino: SCAN_START:
  Arduino: STATUS:Place finger on sensor...
[User places finger]
  Arduino: STATUS:Image taken
  Arduino: STATUS:Image converted
  Arduino: STATUS:Searching for match...
  Arduino: STATUS:Match found!
  Arduino: MATCH_FOUND:1:95

============================================================
🔍 MATCH FOUND!
============================================================
Fingerprint ID:  1
Confidence:      95
Name:            John Doe
Age:             35
Description:     Robbery suspect, case #2024-001
Registered:      2024-01-15T10:30:00
Photo:           /home/user/suspects/john_doe.jpg

[Opening suspect photo...]
============================================================

>
```
*At this point, John Doe's photo opens automatically in your image viewer*

### Scan Unknown Fingerprint (No Match)
```bash
> scan
```

**Output:**
```
🔍 Scanning fingerprint...
Place finger on sensor...
  Arduino: SCAN_START:
  Arduino: STATUS:Place finger on sensor...
[User places finger]
  Arduino: STATUS:Image taken
  Arduino: STATUS:Image converted
  Arduino: STATUS:Searching for match...
  Arduino: MATCH_NOTFOUND:

⚠ No match found in database

>
```

---

## Scenario 3: Database Management

### Add Info to Existing Fingerprint
```bash
# If you enrolled a fingerprint but forgot to add info
> add 1
```

**Output:**
```
📝 Adding suspect information for ID 1:
  Name: John Doe Updated
  Age: 36
  Description: Updated information
  Image path (optional, press Enter to skip): 

✓ Added suspect: John Doe Updated (ID: 1)
✓ Database saved (2 suspects)

>
```

### Delete a Fingerprint and Suspect Data
```bash
> delete 1
```

**Output:**
```
🗑️  Deleting fingerprint ID: 1
  Arduino: DELETE_SUCCESS:1
✓ Fingerprint 1 deleted from sensor
✓ Suspect data removed from database
✓ Database saved (1 suspects)

>
```

---

## Scenario 4: Error Handling

### Enrollment Fails - Fingerprints Don't Match
```bash
> enroll 5
```

**Output:**
```
📝 Enrolling fingerprint ID: 5
Follow the instructions from Arduino...
  Arduino: ENROLL_START:5
  Arduino: STATUS:Place finger on sensor...
  Arduino: STATUS:Image taken
  Arduino: STATUS:Image converted
  Arduino: STATUS:Remove finger
  Arduino: STATUS:Place same finger again...
  Arduino: STATUS:Image taken
  Arduino: STATUS:Image converted
  Arduino: STATUS:Creating model...
  Arduino: ERROR:Fingerprints did not match

>
```

### Sensor Issue - No Finger Detected
```bash
> scan
```

**Output:**
```
🔍 Scanning fingerprint...
Place finger on sensor...
  Arduino: SCAN_START:
  Arduino: STATUS:Place finger on sensor...
  Arduino: ERROR:No finger detected

>
```

### Match Found But No Suspect Data
```bash
> scan
```

**Output:**
```
🔍 Scanning fingerprint...
Place finger on sensor...
  Arduino: SCAN_START:
  Arduino: STATUS:Place finger on sensor...
  Arduino: STATUS:Image taken
  Arduino: STATUS:Image converted
  Arduino: STATUS:Searching for match...
  Arduino: STATUS:Match found!
  Arduino: MATCH_FOUND:3:92

⚠ Match found (ID: 3), but no suspect data available!
   Use 'add' command to register this suspect.

>
```

---

## Scenario 5: Multiple Users in a Shift

### Officer 1 - Morning Shift
```bash
> scan
# Match: John Doe
# Photo opens, officer reviews

> scan
# No match - unknown person
# Officer takes note

> enroll 10
# New suspect arrested
# Officer enrolls and adds info
```

### Officer 2 - Afternoon Shift
```bash
> list
# Reviews all suspects in system

> scan
# Match: Jane Smith
# Photo opens, officer confirms identity

> scan
# Match: New suspect #10 from morning
# Photo opens, officer processes
```

---

## Scenario 6: Bulk Enrollment Session

```bash
# Enrolling multiple suspects in sequence

> enroll 1
[Complete enrollment + info for Suspect 1]

> enroll 2
[Complete enrollment + info for Suspect 2]

> enroll 3
[Complete enrollment + info for Suspect 3]

> enroll 4
[Complete enrollment + info for Suspect 4]

> enroll 5
[Complete enrollment + info for Suspect 5]

> count
📊 Fingerprints stored: 5

> list
[Shows all 5 suspects]
```

---

## Scenario 7: Integration Example (Python Script)

### Custom Automation Script
```python
#!/usr/bin/env python3
from fingerprint_app import FingerprintApp
import time

# Initialize
app = FingerprintApp(port='/dev/ttyUSB0')
app.connect()

# Continuous scanning mode
print("Starting continuous scan mode...")
print("Place finger on sensor to identify...")

while True:
    try:
        # Scan for fingerprint
        matched_id = app.scan_fingerprint()
        
        if matched_id:
            suspect = app.get_suspect(matched_id)
            
            # Log the match
            with open('matches.log', 'a') as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - "
                       f"Match: {suspect['name']} (ID: {matched_id})\n")
            
            # Could trigger other actions:
            # - Send alert
            # - Update external database
            # - Take photo
            # - Sound alarm
            
        time.sleep(2)  # Wait before next scan
        
    except KeyboardInterrupt:
        print("\nStopping...")
        break

app.disconnect()
```

---

## Tips for Best Results

### ✅ DO:
- Clean the sensor before each enrollment
- Use the center of the finger, not the tip
- Press firmly but gently
- Ensure finger is dry
- Use consistent pressure for both enrollment scans
- Wait for status messages before proceeding
- Keep track of which ID corresponds to which finger

### ❌ DON'T:
- Don't move finger during scanning
- Don't press too hard (can distort pattern)
- Don't use wet or very dry fingers
- Don't use the same ID for multiple people
- Don't ignore error messages
- Don't forget to backup the database

---

## Real-World Use Case: Law Enforcement

### Morning Briefing
```bash
> list
# Review all suspects in system
# 25 active suspects listed
```

### Field Operation
```bash
> scan
# Unknown person stopped
# Place finger on portable sensor
# MATCH: Suspect #7 - Wanted for questioning
# Photo displays on tablet
# Officer confirms identity
# Proceeds with protocol
```

### End of Shift
```bash
> enroll 26
# New suspect arrested
# Enroll fingerprint
# Add mugshot and case info
# Database updated for next shift
```

---

**For more information, see:**
- [Complete Guide](docs/GUIDE.md)
- [Quick Reference](QUICKSTART.md)
- [System Architecture](docs/ARCHITECTURE.md)
