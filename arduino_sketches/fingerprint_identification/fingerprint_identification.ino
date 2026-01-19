/*
 * Fingerprint Identification Sketch
 * Phase 2: Real-Time Crime Lab Trigger
 * 
 * This sketch continuously scans for fingerprints and sends a trigger
 * signal to the Mac when a match is found, including confidence score.
 * 
 * Signal Format: FOUND_ID:<id>:<confidence>
 * Example: FOUND_ID:3:215
 * 
 * Close Serial Monitor after uploading so Python can connect!
 * 
 * Wiring: BROWN-5V, ORANGE-GND, BLUE-Pin 2, WHITE-Pin 3
 */

#include <Adafruit_Fingerprint.h>

// Initialize serial communication with the sensor (Pins 2 and 3)
SoftwareSerial mySerial(2, 3);
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);

void setup() {
  Serial.begin(9600); // Mac communication speed
  finger.begin(57600); // Sensor communication speed
  
  // Verify sensor connection
  if (finger.verifyPassword()) {
    Serial.println("READY");
  } else {
    Serial.println("ERROR:SENSOR_NOT_FOUND");
    while (1) { delay(1); }
  }
}

void loop() {
  getFingerprintID();
  delay(50); // Short delay to prevent overwhelming the serial port
}

uint8_t getFingerprintID() {
  uint8_t p = finger.getImage();
  
  // Return silently if no finger detected
  if (p != FINGERPRINT_OK) return p;

  // Convert image to template
  p = finger.image2Tz();
  if (p != FINGERPRINT_OK) return p;

  // Search for a match
  p = finger.fingerFastSearch();
  
  if (p == FINGERPRINT_OK) {
    // Match found! Send trigger to Mac
    Serial.print("FOUND_ID:");
    Serial.print(finger.fingerID);
    Serial.print(":");
    Serial.println(finger.confidence);
    
    // Prevent multiple rapid triggers for the same finger
    delay(3000);
    
    return p;
  } else if (p == FINGERPRINT_NOTFOUND) {
    // No match found (not an error, just no match)
    Serial.println("NO_MATCH");
    delay(1000);
    return p;
  } else {
    // Other errors
    return p;
  }
}
