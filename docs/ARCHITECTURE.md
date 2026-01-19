# System Architecture & Workflow

## System Architecture

```
┌───────────────────────────────────────────────────────────────┐
│                   FINGERPRINT AUTOMATION SYSTEM                │
└───────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  HARDWARE LAYER                                                  │
│                                                                  │
│  ┌──────────────────┐         ┌─────────────────┐              │
│  │  Fingerprint     │ Serial  │    Arduino      │              │
│  │  Sensor          │◄───────►│    Board        │              │
│  │  (AS608/R307)    │ 57600   │  (UNO/Nano/Mega)│              │
│  └──────────────────┘         └────────┬────────┘              │
│                                         │                        │
└─────────────────────────────────────────┼───────────────────────┘
                                          │ USB Serial (9600)
                                          │
┌─────────────────────────────────────────┼───────────────────────┐
│  SOFTWARE LAYER                         │                        │
│                                         ▼                        │
│  ┌────────────────────────────────────────────────────┐         │
│  │         Python Backend Application                 │         │
│  │  ┌──────────────────────────────────────────────┐  │         │
│  │  │  Serial Communication Handler                │  │         │
│  │  │  - Sends: ENROLL, SCAN, DELETE commands      │  │         │
│  │  │  - Receives: MATCH_FOUND, SUCCESS, ERROR     │  │         │
│  │  └──────────────────────────────────────────────┘  │         │
│  │  ┌──────────────────────────────────────────────┐  │         │
│  │  │  Database Manager                            │  │         │
│  │  │  - CRUD operations on suspect data           │  │         │
│  │  │  - JSON file storage                         │  │         │
│  │  └──────────────────────────────────────────────┘  │         │
│  │  ┌──────────────────────────────────────────────┐  │         │
│  │  │  User Interface (CLI)                        │  │         │
│  │  │  - Interactive commands                      │  │         │
│  │  │  - Real-time status updates                  │  │         │
│  │  └──────────────────────────────────────────────┘  │         │
│  │  ┌──────────────────────────────────────────────┐  │         │
│  │  │  Display Handler                             │  │         │
│  │  │  - Shows suspect profile                     │  │         │
│  │  │  - Opens images automatically                │  │         │
│  │  └──────────────────────────────────────────────┘  │         │
│  └────────────────────────────────────────────────────┘         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  DATA LAYER                                                      │
│                                                                  │
│  ┌────────────────────┐      ┌─────────────────────┐           │
│  │ suspects_          │      │  suspect_images/    │           │
│  │ database.json      │      │  - suspect_001.jpg  │           │
│  │                    │      │  - suspect_002.jpg  │           │
│  │ {                  │      │  - ...              │           │
│  │   "1": {           │      └─────────────────────┘           │
│  │     "name": "...", │                                         │
│  │     "age": "...",  │                                         │
│  │     "image_path": "..."                                     │
│  │   }                │                                         │
│  │ }                  │                                         │
│  └────────────────────┘                                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Complete Workflow: Enrollment to Match

```
PHASE 1: ENROLLMENT
═══════════════════

User                Python App           Arduino            Sensor
  │                      │                   │                 │
  ├─► enroll 1          │                   │                 │
  │                      │                   │                 │
  │                      ├──► ENROLL:1      │                 │
  │                      │                   │                 │
  │                      │                   ├──► Initialize   │
  │                      │                   │                 │
  │   ◄────────────────── "Place finger"    │                 │
  │                      │                   │                 │
  ├─► [Places finger]    │                   │                 │
  │                      │                   │   ◄──Capture────┤
  │                      │                   │                 │
  │   ◄────────────────── "Remove finger"   │                 │
  │                      │                   │                 │
  ├─► [Removes finger]   │                   │                 │
  │                      │                   │                 │
  │   ◄────────────────── "Place again"     │                 │
  │                      │                   │                 │
  ├─► [Places finger]    │                   │                 │
  │                      │                   │   ◄──Capture────┤
  │                      │                   │                 │
  │                      │                   ├──► Create model │
  │                      │                   │                 │
  │                      │                   ├──► Store ID:1   │
  │                      │                   │                 │
  │                      │   ◄── SUCCESS:1   │                 │
  │                      │                   │                 │
  │   ◄────────────────── "Enter info"      │                 │
  │                      │                   │                 │
  ├─► Name: John Doe    │                   │                 │
  ├─► Age: 35           │                   │                 │
  ├─► Desc: Suspect...  │                   │                 │
  ├─► Image: photo.jpg  │                   │                 │
  │                      │                   │                 │
  │                      ├──► Save to DB    │                 │
  │                      │                   │                 │
  │   ◄────────────────── "Saved!"          │                 │
  │                      │                   │                 │


PHASE 2: SCANNING & MATCHING
═════════════════════════════

User                Python App           Arduino            Sensor
  │                      │                   │                 │
  ├─► scan              │                   │                 │
  │                      │                   │                 │
  │                      ├──► SCAN          │                 │
  │                      │                   │                 │
  │   ◄────────────────── "Place finger"    │                 │
  │                      │                   │                 │
  ├─► [Places finger]    │                   │                 │
  │                      │                   │   ◄──Capture────┤
  │                      │                   │                 │
  │                      │                   ├──► Convert      │
  │                      │                   │                 │
  │                      │                   ├──► Search DB    │
  │                      │                   │                 │
  │                      │                   ├──► Match! ID:1  │
  │                      │                   │    Conf: 95     │
  │                      │   ◄── MATCH:1:95  │                 │
  │                      │                   │                 │
  │                      ├──► Load from DB   │                 │
  │                      │    (ID: 1)        │                 │
  │                      │                   │                 │
  │   ◄────────────────── Display:          │                 │
  │                      ═══════════════════ │                 │
  │                      MATCH FOUND!        │                 │
  │                      ID: 1               │                 │
  │                      Name: John Doe      │                 │
  │                      Age: 35             │                 │
  │                      Desc: Suspect...    │                 │
  │                      ═══════════════════ │                 │
  │                      │                   │                 │
  │                      ├──► Open photo.jpg │                 │
  │                      │                   │                 │
  │   ◄────────────────── [Photo opens]     │                 │
  │                      │                   │                 │
  │                      ├──► Update last_   │                 │
  │                      │    matched time   │                 │
  │                      │                   │                 │
```

## Data Flow

```
┌────────────────────────────────────────────────────────────┐
│  1. FINGERPRINT CAPTURE                                     │
│                                                             │
│  Finger → Sensor → Image → Template → Arduino Memory       │
│           (optical)  (scan)  (features)    (ID: 1-127)     │
│                                                             │
└────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────┐
│  2. SERIAL COMMUNICATION                                    │
│                                                             │
│  Arduino ←─[USB Serial]─→ Python                           │
│  Commands: ENROLL, SCAN, DELETE, COUNT                     │
│  Responses: SUCCESS, MATCH_FOUND, ERROR                    │
│                                                             │
└────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────┐
│  3. DATA STORAGE                                            │
│                                                             │
│  Python App → JSON File                                    │
│  {                                                          │
│    "fingerprint_id": 1,                                    │
│    "name": "John Doe",                                     │
│    "age": "35",                                            │
│    "description": "Suspect in case #12345",               │
│    "image_path": "/path/to/photo.jpg",                    │
│    "created_at": "2024-01-15T14:30:00",                   │
│    "last_matched": "2024-01-16T09:15:23"                  │
│  }                                                         │
│                                                             │
└────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────┐
│  4. MATCH & DISPLAY                                         │
│                                                             │
│  Match Found → Retrieve Data → Display Info → Open Image   │
│  (ID + Conf)   (from JSON)      (to CLI)      (OS viewer)  │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

## Component Interaction

```
┌─────────────────────────────────────────────────────────────┐
│                     COMPONENT DIAGRAM                        │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐   reads    ┌────────────────┐
│   Arduino    │◄───────────│  Fingerprint   │
│   Firmware   │            │    Sensor      │
│              │   writes   │                │
│              │───────────►│                │
└──────┬───────┘            └────────────────┘
       │
       │ Serial Protocol
       │ (9600 baud)
       │
       ▼
┌──────────────────────────────────────────────┐
│         Python Application                    │
│  ┌──────────────────────────────────────┐   │
│  │  Class: FingerprintApp               │   │
│  │  ┌────────────────────────────────┐  │   │
│  │  │  Methods:                      │  │   │
│  │  │  - connect()                   │  │   │
│  │  │  - enroll_fingerprint()        │  │   │
│  │  │  - scan_fingerprint()          │  │   │
│  │  │  - add_suspect()               │  │   │
│  │  │  - display_suspect()           │  │   │
│  │  │  - save_database()             │  │   │
│  │  │  - load_database()             │  │   │
│  │  └────────────────────────────────┘  │   │
│  └──────────────────────────────────────┘   │
└───────┬──────────────┬───────────────────────┘
        │              │
        │              │
        ▼              ▼
┌──────────────┐  ┌─────────────────┐
│   JSON DB    │  │  Image Files    │
│  suspects_   │  │  suspect_       │
│  database.   │  │  images/        │
│  json        │  │  *.jpg          │
└──────────────┘  └─────────────────┘
```

## Security Flow

```
┌─────────────────────────────────────────────────────────┐
│               SECURITY CONSIDERATIONS                    │
└─────────────────────────────────────────────────────────┘

Fingerprint Template
        │
        ▼
    [Encrypted]
        │
        ▼
    Stored in Sensor
    (Not exported)
        │
        ▼
    Only matching happens
        │
        ▼
    Returns ID only
    (Not template)
        │
        ▼
    Python App uses ID
    to lookup data
        │
        ▼
    Displays suspect info

Note: Raw fingerprint data never leaves the sensor
Only match results (ID + confidence) are transmitted
```

---

This architecture ensures:
- ✅ Secure fingerprint storage
- ✅ Fast matching (< 1 second)
- ✅ Reliable serial communication
- ✅ Persistent data storage
- ✅ Cross-platform compatibility
- ✅ Easy to extend and modify
