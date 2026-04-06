# demo of linked projects::(plssssss see all of these!!!!!!😭)
forensic biometric analyzer demo video::: hardware::: https://vimeo.com/1167734724?fl=ip&fe=ec

Online voting integration with crime scene demo::::     https://birbh.github.io/Online_voting/index.html

Powerpoint pptx for scene:::::          https://jumpshare.com/share/hq6UB4P8KTd2Aa3ldhZg

# Crime Lab Fingerprint Automation System

Fingerprint identification with a small web app and optional GSR (stress) sensor. When a match is detected, the browser shows a suspect dossier and a live GSR graph.

# Integration

This project is integrated with [online_voting](https://github.com/birbh/Online_voting/). This is the voting system for criminals where users can also state their reason for their vote, enabling interactive user engagement within the crime lab ecosystem.

Also a powerpoint ppt for this scene is also available at link::: [PPtx](https://jumpshare.com/share/hq6UB4P8KTd2Aa3ldhZg)

## Features

- Fingerprint match detection and logging
- Live GSR graph from Arduino A0
- WebSocket updates for live UI
- MySQL storage for suspects, match history, and GSR sessions

## Docs

- [QUICKSTART.md](QUICKSTART.md)
- [SETUP_GUIDE.md](SETUP_GUIDE.md)

## Quick Start

1. Install MySQL and Python packages.
2. Run schema: `mysql -u root -p < database/schema.sql`
3. Set DB password in `web_app/app.py`.
4. Wire fingerprint sensor + GSR sensor to Arduino.
5. Upload enrollment sketch and enroll fingerprints.
6. Start server: `cd web_app && python3 app.py`
7. Start listener: `python3 serial_listener.py`
8. Upload identification sketch.
      


## Demo:::::

https://github.com/user-attachments/assets/b0b8699c-f369-49b5-bcb0-6223d8319270


See [SETUP_GUIDE.md](SETUP_GUIDE.md) for full instructions.
