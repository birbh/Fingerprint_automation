/*
 * Fingerprint Enrollment Sketch
 * Phase 1: Store Suspects in the Sensor Memory
 * 
 * This sketch allows you to scan and store fingerprints with IDs 1-200
 * Upload this code, open Serial Monitor, and type the ID number to enroll.
 * 
 * Wiring: BROWN-5V, ORANGE-GND, BLUE-Pin 2, WHITE-Pin 3
 */

#include <Adafruit_Fingerprint.h>

// Initialize serial communication with the sensor (Pins 2 and 3)
SoftwareSerial mySerial(2, 3);
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);

uint8_t id;

void setup() {
  Serial.begin(9600);
  while (!Serial);
  delay(100);
  
  Serial.println("\n=== Fingerprint Enrollment System ===");
  Serial.println("Crime Lab - Suspect Registration");
  
  // Set the data rate for the sensor serial port
  finger.begin(57600);
  
  if (finger.verifyPassword()) {
    Serial.println("✓ Sensor connected successfully!");
  } else {
    Serial.println("✗ Sensor not found. Check wiring!");
    while (1) { delay(1); }
  }
  
  Serial.println("\nReady to enroll suspects.");
  Serial.println("Type an ID number (1-200) and press Enter.");
}

void loop() {
  Serial.println("\n>>> Enter Suspect ID to enroll (1-200): ");
  
  id = readnumber();
  if (id == 0) {
    return;
  }
  
  Serial.print("Enrolling Suspect ID #");
  Serial.println(id);
  
  while (!getFingerprintEnroll());
}

uint8_t readnumber(void) {
  uint8_t num = 0;
  
  while (num == 0) {
    while (!Serial.available());
    num = Serial.parseInt();
  }
  return num;
}

uint8_t getFingerprintEnroll() {
  int p = -1;
  
  Serial.print("Place finger on sensor for Suspect ID #");
  Serial.println(id);
  
  while (p != FINGERPRINT_OK) {
    p = finger.getImage();
    switch (p) {
      case FINGERPRINT_OK:
        Serial.println("✓ Image captured");
        break;
      case FINGERPRINT_NOFINGER:
        break;
      case FINGERPRINT_PACKETRECIEVEERR:
        Serial.println("✗ Communication error");
        break;
      case FINGERPRINT_IMAGEFAIL:
        Serial.println("✗ Imaging error");
        break;
      default:
        Serial.println("✗ Unknown error");
        break;
    }
  }

  // Convert image to template
  p = finger.image2Tz(1);
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("✓ Image converted");
      break;
    case FINGERPRINT_IMAGEMESS:
      Serial.println("✗ Image too messy");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("✗ Communication error");
      return p;
    case FINGERPRINT_FEATUREFAIL:
      Serial.println("✗ Could not find fingerprint features");
      return p;
    case FINGERPRINT_INVALIDIMAGE:
      Serial.println("✗ Invalid image");
      return p;
    default:
      Serial.println("✗ Unknown error");
      return p;
  }

  Serial.println("Remove finger");
  delay(1000);
  
  
  
  Serial.print("Place SAME finger again for verification");
  p = -1;
  
  while (p != FINGERPRINT_OK) {
    p = finger.getImage();
    switch (p) {
      case FINGERPRINT_OK:
        Serial.println("✓ Image captured");
        break;
      case FINGERPRINT_NOFINGER:
        break;
      case FINGERPRINT_PACKETRECIEVEERR:
        Serial.println("✗ Communication error");
        break;
      case FINGERPRINT_IMAGEFAIL:
        Serial.println("✗ Imaging error");
        break;
      default:
        Serial.println("✗ Unknown error");
        break;
    }
  }

  // Convert second image
  p = finger.image2Tz(2);
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("✓ Image converted");
      break;
    case FINGERPRINT_IMAGEMESS:
      Serial.println("✗ Image too messy");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("✗ Communication error");
      return p;
    case FINGERPRINT_FEATUREFAIL:
      Serial.println("✗ Could not find fingerprint features");
      return p;
    case FINGERPRINT_INVALIDIMAGE:
      Serial.println("✗ Invalid image");
      return p;
    default:
      Serial.println("✗ Unknown error");
      return p;
  }

  // Create model
  Serial.print("Creating model for Suspect #");
  Serial.println(id);
  
  p = finger.createModel();
  if (p == FINGERPRINT_OK) {
    Serial.println("✓ Prints matched!");
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    Serial.println("✗ Communication error");
    return p;
  } else if (p == FINGERPRINT_ENROLLMISMATCH) {
    Serial.println("✗ Fingerprints did not match. Try again.");
    return p;
  } else {
    Serial.println("✗ Unknown error");
    return p;
  }

  // Store model
  Serial.print("Storing model with ID #");
  Serial.println(id);
  
  p = finger.storeModel(id);
  if (p == FINGERPRINT_OK) {
    Serial.println("✓✓✓ SUSPECT ENROLLED SUCCESSFULLY! ✓✓✓");
    Serial.print("Suspect ID #");
    Serial.print(id);
    Serial.println(" is now in the database.");
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    Serial.println("✗ Communication error");
    return p;
  } else if (p == FINGERPRINT_BADLOCATION) {
    Serial.println("✗ Could not store in that location");
    return p;
  } else if (p == FINGERPRINT_FLASHERR) {
    Serial.println("✗ Error writing to flash");
    return p;
  } else {
    Serial.println("✗ Unknown error");
    return p;
  }

  return true;
}
