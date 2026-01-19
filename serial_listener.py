"""
Serial Listener - Arduino to Web Bridge
Listens for fingerprint match signals from Arduino and triggers web dossier display
"""

import serial
import requests
import webbrowser
import time
import sys
import os

# ============================================
# Configuration
# ============================================

# Arduino serial port - Change this to match your Arduino port
# To find your port:
# 1. Open Arduino IDE
# 2. Go to Tools > Port
# 3. Copy the port name (e.g., /dev/cu.usbmodem1101)
ARDUINO_PORT = "/dev/cu.usbserial-A5069RR4"  # <-- CHANGE THIS
BAUD_RATE = 9600

# Flask server URL
FLASK_URL = "http://localhost:5001"

# ============================================
# Functions
# ============================================

def connect_arduino():
    """Connect to Arduino serial port"""
    try:
        ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Wait for Arduino to reset
        print("✓ Connected to Arduino")
        print(f"  Port: {ARDUINO_PORT}")
        print(f"  Baud Rate: {BAUD_RATE}")
        return ser
    except serial.SerialException as e:
        print(f"✗ Could not connect to Arduino: {e}")
        print("\nTroubleshooting:")
        print("1. Check that Arduino is plugged in")
        print("2. Close Arduino IDE Serial Monitor if open")
        print("3. Verify the port name in this script matches Arduino IDE")
        print("4. Try a different USB cable or port")
        sys.exit(1)

def check_flask_server():
    """Check if Flask server is running"""
    try:
        response = requests.get(FLASK_URL, timeout=2)
        print("✓ Flask server is running")
        return True
    except requests.exceptions.RequestException:
        print("✗ Flask server not responding")
        print("\nPlease start the Flask server first:")
        print("  cd web_app")
        print("  python3 app.py")
        return False

def log_match(suspect_id, confidence):
    """Send match data to Flask API"""
    try:
        response = requests.post(
            f"{FLASK_URL}/api/log-match",
            json={
                "suspect_id": suspect_id,
                "confidence": confidence
            },
            timeout=5
        )
        if response.status_code == 200:
            print(f"✓ Match logged to database")
            return True
        else:
            print(f"✗ Failed to log match: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Error logging match: {e}")
        return False

def open_dossier(suspect_id):
    """Open suspect dossier in default browser"""
    url = f"{FLASK_URL}/suspect/{suspect_id}"
    try:
        webbrowser.open(url)
        print(f"✓ Opening dossier in browser: {url}")
        return True
    except Exception as e:
        print(f"✗ Error opening browser: {e}")
        return False

def parse_arduino_signal(line):
    """
    Parse Arduino signal
    Format: FOUND_ID:<id>:<confidence>
    Example: FOUND_ID:3:215
    """
    if not line.startswith("FOUND_ID:"):
        return None, None
    
    try:
        parts = line.split(":")
        suspect_id = int(parts[1])
        confidence = int(parts[2])
        return suspect_id, confidence
    except (IndexError, ValueError):
        print(f"✗ Invalid signal format: {line}")
        return None, None

# ============================================
# Main Loop
# ============================================

def main():
    print("=" * 60)
    print("CRIME LAB - Serial Listener")
    print("Fingerprint Match Detection System")
    print("=" * 60)
    print()
    
    # Check Flask server
    if not check_flask_server():
        print("\n⚠️  Warning: Flask server not running!")
        print("Starting anyway, but matches won't be logged until server is started.")
        print()
    
    # Connect to Arduino
    ser = connect_arduino()
    print()
    print("=" * 60)
    print("🔍 SYSTEM ACTIVE - Waiting for fingerprint matches...")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    print()
    
    last_match_time = 0
    cooldown_seconds = 3  # Prevent duplicate triggers
    
    try:
        while True:
            if ser.in_waiting > 0:
                try:
                    # Read line from Arduino
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    
                    if not line:
                        continue
                    
                    # Print all Arduino messages for debugging
                    print(f"[Arduino] {line}")
                    
                    # Check for match signal
                    if "FOUND_ID:" in line:
                        suspect_id, confidence = parse_arduino_signal(line)
                        
                        if suspect_id is None:
                            continue
                        
                        # Prevent duplicate triggers within cooldown period
                        current_time = time.time()
                        if current_time - last_match_time < cooldown_seconds:
                            print(f"  (Cooldown active - ignoring)")
                            continue
                        
                        last_match_time = current_time
                        
                        print()
                        print("=" * 60)
                        print("🚨 FINGERPRINT MATCH DETECTED! 🚨")
                        print("=" * 60)
                        print(f"  Suspect ID: {suspect_id}")
                        print(f"  Confidence: {confidence}/255 ({confidence/255*100:.1f}%)")
                        print()
                        
                        # Log to database
                        log_match(suspect_id, confidence)
                        
                        # Open browser
                        open_dossier(suspect_id)
                        
                        print()
                        print("=" * 60)
                        print("Waiting for next match...")
                        print("=" * 60)
                        print()
                    
                    elif line == "NO_MATCH":
                        print("  → No match found in database")
                    
                    elif line == "READY":
                        print("  → Arduino sensor initialized")
                
                except UnicodeDecodeError:
                    pass  # Ignore decode errors
                except Exception as e:
                    print(f"Error processing line: {e}")
            
            time.sleep(0.1)  # Small delay to prevent CPU overuse
    
    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("System stopped by user")
        print("=" * 60)
        ser.close()
        sys.exit(0)
    
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        ser.close()
        sys.exit(1)

if __name__ == "__main__":
    main()
