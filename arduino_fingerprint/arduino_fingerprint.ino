/*
 * Fingerprint Automation System - Arduino Sketch
 * This sketch interfaces with the fingerprint sensor (e.g., AS608/R307)
 * and communicates with a Python application via serial connection
 */

#include <Adafruit_Fingerprint.h>

// Pin configuration for software serial (for Arduino UNO/Nano)
// For Arduino Mega, you can use Serial1, Serial2, etc.
#if defined(__AVR_ATmega2560__)
  #define mySerial Serial1
#else
  #include <SoftwareSerial.h>
  SoftwareSerial mySerial(2, 3);  // RX=2, TX=3
#endif

Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);

uint8_t id;

void setup() {
  Serial.begin(9600);
  while (!Serial);  // Wait for serial to be ready
  delay(100);
  
  Serial.println("Fingerprint Automation System");
  Serial.println("==============================");
  
  // Initialize sensor at baud rate 57600
  finger.begin(57600);
  
  if (finger.verifyPassword()) {
    Serial.println("READY:Fingerprint sensor found!");
  } else {
    Serial.println("ERROR:Fingerprint sensor not found!");
    while (1) { delay(1); }
  }
  
  Serial.println("MENU:Ready for commands");
  printMenu();
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    
    if (command.startsWith("ENROLL:")) {
      // Extract ID from command (format: ENROLL:1)
      int colonPos = command.indexOf(':');
      if (colonPos != -1) {
        id = command.substring(colonPos + 1).toInt();
        enrollFingerprint();
      }
    } else if (command == "SCAN") {
      scanFingerprint();
    } else if (command == "COUNT") {
      getTemplateCount();
    } else if (command.startsWith("DELETE:")) {
      int colonPos = command.indexOf(':');
      if (colonPos != -1) {
        id = command.substring(colonPos + 1).toInt();
        deleteFingerprint();
      }
    } else if (command == "EMPTY") {
      emptyDatabase();
    } else if (command == "MENU") {
      printMenu();
    } else {
      Serial.println("ERROR:Unknown command");
      printMenu();
    }
  }
  
  delay(50);
}

void printMenu() {
  Serial.println("\nAvailable Commands:");
  Serial.println("  ENROLL:ID - Enroll fingerprint with ID (e.g., ENROLL:1)");
  Serial.println("  SCAN - Scan and match fingerprint");
  Serial.println("  COUNT - Get stored fingerprint count");
  Serial.println("  DELETE:ID - Delete fingerprint with ID");
  Serial.println("  EMPTY - Clear all fingerprints");
  Serial.println("  MENU - Show this menu");
}

uint8_t enrollFingerprint() {
  int p = -1;
  Serial.print("ENROLL_START:");
  Serial.println(id);
  Serial.println("STATUS:Place finger on sensor...");
  
  while (p != FINGERPRINT_OK) {
    p = finger.getImage();
    switch (p) {
      case FINGERPRINT_OK:
        Serial.println("STATUS:Image taken");
        break;
      case FINGERPRINT_NOFINGER:
        break;
      case FINGERPRINT_PACKETRECIEVEERR:
        Serial.println("ERROR:Communication error");
        return p;
      case FINGERPRINT_IMAGEFAIL:
        Serial.println("ERROR:Imaging error");
        return p;
      default:
        Serial.println("ERROR:Unknown error");
        return p;
    }
  }
  
  // Convert image
  p = finger.image2Tz(1);
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("STATUS:Image converted");
      break;
    case FINGERPRINT_IMAGEMESS:
      Serial.println("ERROR:Image too messy");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("ERROR:Communication error");
      return p;
    case FINGERPRINT_FEATUREFAIL:
      Serial.println("ERROR:Could not find fingerprint features");
      return p;
    case FINGERPRINT_INVALIDIMAGE:
      Serial.println("ERROR:Invalid image");
      return p;
    default:
      Serial.println("ERROR:Unknown error");
      return p;
  }
  
  Serial.println("STATUS:Remove finger");
  delay(2000);
  p = 0;
  while (p != FINGERPRINT_NOFINGER) {
    p = finger.getImage();
  }
  
  Serial.println("STATUS:Place same finger again...");
  p = -1;
  while (p != FINGERPRINT_OK) {
    p = finger.getImage();
    switch (p) {
      case FINGERPRINT_OK:
        Serial.println("STATUS:Image taken");
        break;
      case FINGERPRINT_NOFINGER:
        break;
      case FINGERPRINT_PACKETRECIEVEERR:
        Serial.println("ERROR:Communication error");
        return p;
      case FINGERPRINT_IMAGEFAIL:
        Serial.println("ERROR:Imaging error");
        return p;
      default:
        Serial.println("ERROR:Unknown error");
        return p;
    }
  }
  
  // Convert second image
  p = finger.image2Tz(2);
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("STATUS:Image converted");
      break;
    case FINGERPRINT_IMAGEMESS:
      Serial.println("ERROR:Image too messy");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("ERROR:Communication error");
      return p;
    case FINGERPRINT_FEATUREFAIL:
      Serial.println("ERROR:Could not find fingerprint features");
      return p;
    case FINGERPRINT_INVALIDIMAGE:
      Serial.println("ERROR:Invalid image");
      return p;
    default:
      Serial.println("ERROR:Unknown error");
      return p;
  }
  
  // Create model
  Serial.println("STATUS:Creating model...");
  p = finger.createModel();
  if (p == FINGERPRINT_OK) {
    Serial.println("STATUS:Prints matched!");
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    Serial.println("ERROR:Communication error");
    return p;
  } else if (p == FINGERPRINT_ENROLLMISMATCH) {
    Serial.println("ERROR:Fingerprints did not match");
    return p;
  } else {
    Serial.println("ERROR:Unknown error");
    return p;
  }
  
  // Store model
  Serial.print("STATUS:Storing model #");
  Serial.println(id);
  p = finger.storeModel(id);
  if (p == FINGERPRINT_OK) {
    Serial.print("ENROLL_SUCCESS:");
    Serial.println(id);
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    Serial.println("ERROR:Communication error");
    return p;
  } else if (p == FINGERPRINT_BADLOCATION) {
    Serial.println("ERROR:Could not store in that location");
    return p;
  } else if (p == FINGERPRINT_FLASHERR) {
    Serial.println("ERROR:Error writing to flash");
    return p;
  } else {
    Serial.println("ERROR:Unknown error");
    return p;
  }
  
  return true;
}

uint8_t scanFingerprint() {
  Serial.println("SCAN_START:");
  Serial.println("STATUS:Place finger on sensor...");
  
  uint8_t p = finger.getImage();
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("STATUS:Image taken");
      break;
    case FINGERPRINT_NOFINGER:
      Serial.println("ERROR:No finger detected");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("ERROR:Communication error");
      return p;
    case FINGERPRINT_IMAGEFAIL:
      Serial.println("ERROR:Imaging error");
      return p;
    default:
      Serial.println("ERROR:Unknown error");
      return p;
  }
  
  // Convert image
  p = finger.image2Tz();
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("STATUS:Image converted");
      break;
    case FINGERPRINT_IMAGEMESS:
      Serial.println("ERROR:Image too messy");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("ERROR:Communication error");
      return p;
    case FINGERPRINT_FEATUREFAIL:
      Serial.println("ERROR:Could not find fingerprint features");
      return p;
    case FINGERPRINT_INVALIDIMAGE:
      Serial.println("ERROR:Invalid image");
      return p;
    default:
      Serial.println("ERROR:Unknown error");
      return p;
  }
  
  // Search for match
  Serial.println("STATUS:Searching for match...");
  p = finger.fingerSearch();
  if (p == FINGERPRINT_OK) {
    Serial.println("STATUS:Match found!");
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    Serial.println("ERROR:Communication error");
    return p;
  } else if (p == FINGERPRINT_NOTFOUND) {
    Serial.println("MATCH_NOTFOUND:");
    return p;
  } else {
    Serial.println("ERROR:Unknown error");
    return p;
  }
  
  // Found a match!
  Serial.print("MATCH_FOUND:");
  Serial.print(finger.fingerID);
  Serial.print(":");
  Serial.println(finger.confidence);
  
  return finger.fingerID;
}

void getTemplateCount() {
  finger.getTemplateCount();
  Serial.print("COUNT:");
  Serial.println(finger.templateCount);
}

uint8_t deleteFingerprint() {
  uint8_t p = finger.deleteModel(id);
  
  if (p == FINGERPRINT_OK) {
    Serial.print("DELETE_SUCCESS:");
    Serial.println(id);
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    Serial.println("ERROR:Communication error");
    return p;
  } else if (p == FINGERPRINT_BADLOCATION) {
    Serial.println("ERROR:Could not delete in that location");
    return p;
  } else if (p == FINGERPRINT_FLASHERR) {
    Serial.println("ERROR:Error writing to flash");
    return p;
  } else {
    Serial.println("ERROR:Unknown error");
    return p;
  }
  
  return p;
}

void emptyDatabase() {
  Serial.println("STATUS:Clearing database...");
  uint8_t p = finger.emptyDatabase();
  
  if (p == FINGERPRINT_OK) {
    Serial.println("EMPTY_SUCCESS:");
  } else {
    Serial.println("ERROR:Failed to clear database");
  }
  
  return;
}
