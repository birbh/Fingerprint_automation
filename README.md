# 🔍 Crime Lab Fingerprint Automation System

A complete forensic fingerprint identification system that automatically displays criminal dossiers when a match is detected, with integrated live polygraph (GSR) stress detection.

## Features

- **Real-time fingerprint matching** with Arduino fingerprint sensor
- **Live polygraph (GSR) stress detection** with real-time graph display
- **Automatic dossier display** in web browser with suspect information
- **WebSocket live updates** for instant refresh and real-time data streaming
- **Auto-calibrated baseline** from first 10 GSR readings for accuracy
- **Color-coded confidence scores** for fingerprint matches (green/yellow/red)
- **MySQL database** for suspect records, match history, and GSR session data
- **Professional crime lab interface** with mugshots, charges, aliases, and arrest history

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete documentation with troubleshooting

## Quick Start

1. Install MySQL and Python dependencies
2. Run database schema: `mysql -u root -p < database/schema.sql` (includes gsr_sessions table)
3. Configure `web_app/app.py` with your MySQL password
4. Wire fingerprint sensor + GSR sensor to Arduino (see SETUP_GUIDE.md)
5. Upload Arduino enrollment sketch and scan fingerprints
6. Start web server: `cd web_app && python3 app.py`
7. Start serial listener: `python3 serial_listener.py`
8. Upload identification sketch to Arduino
9. Place finger on sensor → dossier opens with live GSR graph!

## 📁 Project Structure

```
├── arduino_sketches/          # Arduino .ino files
│   ├── fingerprint_enrollment/
│   └── fingerprint_identification/
├── web_app/                   # Flask web server
│   ├── app.py
│   └── templates/
├── suspects_images/           # Mugshot photos
├── database/                  # MySQL schema
├── serial_listener.py         # Arduino-to-web bridge
└── requirements.txt           # Python dependencies
```

Demo:::::

https://github.com/user-attachments/assets/b0b8699c-f369-49b5-bcb0-6223d8319270


##  Perfect for Science Fairs

Demonstrates:
- Biometric security systems
- Real-time data processing
- Full-stack development (hardware + software + database + web)
- Forensic science applications

---

**See [SETUP_GUIDE.md](SETUP_GUIDE.md) for complete instructions.**
