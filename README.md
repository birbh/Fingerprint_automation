# 🔍 Crime Lab Fingerprint Automation System

A complete forensic fingerprint identification system that automatically displays criminal dossiers when a match is detected.

## 🎯 Features

- **Real-time fingerprint matching** with Arduino sensor
- **Automatic dossier display** in web browser
- **WebSocket live updates** for instant refresh
- **Color-coded confidence scores** (green/yellow/red)
- **MySQL database** for suspect records and match history
- **Professional crime lab interface** with mugshots, charges, aliases, and arrest history

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete documentation with troubleshooting

## 🚀 Quick Start

1. Install MySQL and Python dependencies
2. Run database schema: `mysql -u root -p < database/schema.sql`
3. Configure `web_app/app.py` with your MySQL password
4. Upload Arduino enrollment sketch and scan fingerprints
5. Start web server: `cd web_app && python3 app.py`
6. Start serial listener: `python3 serial_listener.py`
7. Upload identification sketch to Arduino
8. Place finger on sensor → dossier opens automatically!

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

## 🎓 Perfect for Science Fairs

Demonstrates:
- Biometric security systems
- Real-time data processing
- Full-stack development (hardware + software + database + web)
- Forensic science applications

---

**See [SETUP_GUIDE.md](SETUP_GUIDE.md) for complete instructions.**