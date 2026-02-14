# Circuit Wiring Information

Basic wiring for a fingerprint sensor and a GSR sensor with Arduino Uno. Pin colors may vary by sensor model. Check your sensor's datasheet.

---

## Components Required

- **Arduino Uno** (or compatible board)
- **Fingerprint Sensor** (Adafruit-compatible, e.g., AS608, R307, R305, GT-511C3)
- **GSR Sensor** (Galvanic Skin Response/Polygraph sensor with analog output)
- **Jumper Wires** (Male-to-Female recommended)
- **USB Cable** (Type A to Type B for Arduino)
- **Breadboard** (optional, for organizing connections)

---

## Fingerprint Sensor Wiring

### Standard 4-wire Sensor

Most Adafruit fingerprint sensors use the following color-coded wires:

| **Wire Color** | **Connection** | **Arduino Pin** |
|---|---|---|
| 🔴 RED         | Power (+5V)    | 5V              |
| 🟢 GREEN       | Ground (GND)   | GND             |
| 🟡 YELLOW      | RX (Receive)   | Pin 2 (TX)      |
| ⚫ BLACK       | TX (Transmit)  | Pin 3 (RX)      |

### Detailed Connections:

1. **RED wire → Arduino 5V pin**
   - Provides 5V power to the sensor
   - Ensure stable power supply (USB or external adapter)

2. **GREEN wire → Arduino GND pin**
   - Common ground connection
   - Critical for proper communication

3. **YELLOW wire → Arduino Digital Pin 2**
   - Sensor's RX (receives data from Arduino TX)
   - Used by SoftwareSerial library

4. **BLACK wire → Arduino Digital Pin 3**
   - Sensor's TX (transmits data to Arduino RX)
   - Used by SoftwareSerial library

### Alternative Sensor Models

If your sensor has different colored wires, refer to its datasheet for pinout. Common variations:

| **Sensor Model** | **Power** | **Ground** | **RX** | **TX** |
|------------------|-----------|------------|--------|--------|
| AS608            | Red       | Black      | Yellow | Green  |
| R307/R305        | Red       | Black      | White  | Green  |
| GT-511C3         | Red       | Black      | Blue   | White  |

Note: some sensors use 3.3V instead of 5V.

---

## GSR Sensor Wiring

The GSR (Galvanic Skin Response) sensor measures skin conductance for stress/lie detection.

### Standard GSR Sensor (3-wire)

| **Wire/Label** | **Connection** | **Arduino Pin** |
|----------------|----------------|-----------------|
| VCC / +        | Power (+5V)    | 5V              |
| GND / -        | Ground (GND)   | GND             |
| SIG / OUT / A  | Analog Signal  | A0              |

### Detailed Connections:

1. **VCC/+ → Arduino 5V pin**
   - Powers the GSR sensor module
   - Some modules may accept 3.3V-5V range

2. **GND/- → Arduino GND pin**
   - Ground reference for signal

3. **SIG/OUT/A → Arduino Analog Pin A0**
   - Analog output (0-1023 range)
   - Higher values = higher skin conductance (stress)

### GSR Sensor Finger Clips

- Attach the two finger electrodes/clips to the subject's fingers (typically index and middle finger)
- Ensure good skin contact for accurate readings
- Clean electrodes regularly with isopropyl alcohol

---

## Visual Wiring Diagram

```
Arduino Uno
┌─────────────────────┐
│                     │
│  [5V]──┬──────────→ RED (Fingerprint Sensor)
│        └──────────→ VCC (GSR Sensor)
│                     │
│  [GND]─┬──────────→ GREEN (Fingerprint Sensor)
│        └──────────→ GND (GSR Sensor)
│                     │
│  [Pin 2]──────────→ YELLOW (Fingerprint RX)
│  [Pin 3]──────────→ BLACK (Fingerprint TX)
│                     │
│  [A0]─────────────→ SIG (GSR Analog Out)
│                     │
│  [USB]─────────────→ Computer
│                     │
└─────────────────────┘
```

---

## Testing Your Connections

### 1. Test Fingerprint Sensor

Upload the **fingerprint_enrollment.ino** sketch and open Serial Monitor:

```bash
# Expected output:
=== Fingerprint Enrollment System ===
Crime Lab - Suspect Registration
✓ Sensor connected successfully!
```

If you see "Sensor not found", check:
- Power connections (RED to 5V, GREEN to GND)
- Data connections (YELLOW to Pin 2, BLACK to Pin 3)
- Sensor is powered on (LED should light up)

### 2. Test GSR Sensor

Upload the **fingerprint_identification.ino** sketch and open Serial Monitor:

```bash
# Expected output (streaming every 500ms):
READY
GSR_VAL:327
GSR_VAL:331
GSR_VAL:329
```

If GSR values are stuck at 0 or 1023:
- Check analog pin connection (A0)
- Verify power connections (VCC, GND)
- Ensure finger clips are attached to skin

---

## Troubleshooting

### Fingerprint Sensor Issues

| **Problem** | **Solution** |
|-------------|--------------|
| "Sensor not found" | Verify 5V/GND, swap RX/TX pins (try Pin 3↔Pin 2), check baud rate (57600) |
| No fingerprint detected | Clean sensor glass, press finger firmly, check LED indicator |
| Poor match accuracy | Re-enroll fingerprints with multiple angles, clean sensor |
| Communication errors | Check jumper wires for loose connections, avoid long wires (>30cm) |

### GSR Sensor Issues

| **Problem** | **Solution** |
|-------------|--------------|
| GSR_VAL always 0 | Check A0 connection, verify VCC/GND, test with multimeter |
| GSR_VAL always 1023 | Sensor may be disconnected or faulty, check signal wire |
| Erratic readings | Clean finger clips, ensure good skin contact, remove hand lotion |
| No stress detected | Baseline calibration needed (first 10 readings), increase sensitivity threshold |

---

## Power Considerations

### USB Power (Recommended for Testing)
- Arduino USB port provides 500mA
- Sufficient for fingerprint sensor (100-150mA) + GSR sensor (10-20mA)
- Stable for development and testing

### External Power (Recommended for Deployment)
- Use 7-12V DC adapter to Arduino barrel jack
- Provides more stable 5V rail for sensors
- Better for continuous operation

### Power Consumption Estimate:
- Arduino Uno: ~50mA
- Fingerprint Sensor: 100-150mA (120mA active scan)
- GSR Sensor: 10-20mA
- **Total: ~170-220mA** (well within USB limits)

---

## Advanced Configuration

### Using Different Arduino Pins

If Pins 2 and 3 are occupied, you can change the fingerprint sensor pins:

1. Modify the Arduino sketch:
```cpp
// Change from Pin 2,3 to Pin 4,5
SoftwareSerial mySerial(4, 5);  // RX, TX
```

2. Update your physical wiring accordingly
3. Re-upload the sketch

### Using Hardware Serial (Mega/Leonardo)

Arduino Mega/Leonardo have additional hardware serial ports:

```cpp
// Replace SoftwareSerial with:
#define mySerial Serial1  // Use Serial1, Serial2, or Serial3
```

Wiring for Mega Serial1:
- Sensor RX → Pin 19 (TX1)
- Sensor TX → Pin 18 (RX1)

---

## Recommended Components

### Fingerprint Sensors (Tested Compatible)
- Adafruit Fingerprint Sensor (Product ID: 751)
- HiLetgo AS608 Optical Fingerprint Module
- R305 Fingerprint Identification Module
- R307 Capacitive Fingerprint Module

### GSR Sensors (Tested Compatible)
- Grove GSR Sensor (Seeed Studio)
- DIY GSR Sensor Module (Generic)
- E-Health Sensor Platform GSR Module

---

## Resources

- [Adafruit Fingerprint Sensor Guide](https://learn.adafruit.com/adafruit-optical-fingerprint-sensor)
- [Arduino SoftwareSerial Library](https://www.arduino.cc/en/Reference/SoftwareSerial)
- [GSR Sensor Theory](https://en.wikipedia.org/wiki/Electrodermal_activity)
- [Arduino Analog Input Tutorial](https://www.arduino.cc/en/Tutorial/BuiltInExamples/AnalogInput)

---

## Safety Warnings

1. **Never connect sensors to AC power** - Use only DC 5V
2. **Check polarity** - Reversed power can damage sensors
3. **GSR sensors are NOT medical devices** - For educational/demonstration purposes only
4. **Avoid ESD damage** - Handle sensors on anti-static surfaces
5. **Proper ventilation** - Ensure Arduino has adequate cooling during extended use

---

## Notes

- This guide assumes **Arduino Uno** board. Pin assignments may differ for other boards (Mega, Nano, ESP32, etc.)
- **Sensor compatibility varies** - Always verify with manufacturer documentation
- **Serial baud rates matter** - Ensure Arduino sketch matches sensor specs (typically 57600 for fingerprint sensors)
- **Testing recommended** - Verify each sensor individually before running full system

---

## Need Help?

If you encounter issues not covered here:

1. Check the main **[SETUP_GUIDE.md](../../SETUP_GUIDE.md)** for software configuration
2. Verify **[QUICKSTART.md](../../QUICKSTART.md)** for system overview
3. Consult your specific sensor's datasheet
4. Test sensors with standalone Arduino examples first

---

Last updated: January 2026
Compatible with: Arduino Uno, Nano, Mega (with pin adjustments)
