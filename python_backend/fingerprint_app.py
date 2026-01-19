#!/usr/bin/env python3
"""
Fingerprint Automation System - Python Backend
This application manages suspect data and communicates with Arduino
"""

import serial
import json
import os
import sys
import time
import platform
import subprocess
from pathlib import Path
from datetime import datetime
import threading

class FingerprintApp:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
        """
        Initialize the Fingerprint Application
        
        Args:
            port: Serial port connected to Arduino (e.g., COM3 on Windows, /dev/ttyUSB0 on Linux)
            baudrate: Serial communication speed
        """
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.suspects_db = {}
        self.db_file = Path(__file__).parent / 'suspects_database.json'
        self.images_dir = Path(__file__).parent / 'suspect_images'
        
        # Create directories if they don't exist
        self.images_dir.mkdir(exist_ok=True)
        
        # Load existing database
        self.load_database()
        
    def connect(self):
        """Connect to Arduino via serial port"""
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # Wait for Arduino to reset
            print(f"✓ Connected to Arduino on {self.port}")
            
            # Read initial messages from Arduino
            time.sleep(1)
            while self.ser.in_waiting:
                line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                print(f"  Arduino: {line}")
            
            return True
        except serial.SerialException as e:
            print(f"✗ Failed to connect to Arduino: {e}")
            print("\nTroubleshooting:")
            print("  1. Check if Arduino is connected")
            print("  2. Verify the correct port (use 'ls /dev/tty*' on Linux/Mac or Device Manager on Windows)")
            print("  3. Make sure no other application is using the port")
            return False
    
    def disconnect(self):
        """Disconnect from Arduino"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("✓ Disconnected from Arduino")
    
    def send_command(self, command):
        """Send command to Arduino"""
        if self.ser and self.ser.is_open:
            self.ser.write(f"{command}\n".encode())
            time.sleep(0.1)
    
    def read_response(self, timeout=30):
        """Read response from Arduino"""
        responses = []
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.ser.in_waiting:
                line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    responses.append(line)
                    print(f"  Arduino: {line}")
                    
                    # Check for completion messages
                    if any(keyword in line for keyword in ['SUCCESS', 'ERROR', 'NOTFOUND', 'COUNT:']):
                        return responses
            time.sleep(0.1)
        
        return responses
    
    def load_database(self):
        """Load suspects database from JSON file"""
        if self.db_file.exists():
            with open(self.db_file, 'r') as f:
                self.suspects_db = json.load(f)
            print(f"✓ Loaded {len(self.suspects_db)} suspects from database")
        else:
            print("ℹ No existing database found, starting fresh")
    
    def save_database(self):
        """Save suspects database to JSON file"""
        with open(self.db_file, 'w') as f:
            json.dump(self.suspects_db, indent=2, fp=f)
        print(f"✓ Database saved ({len(self.suspects_db)} suspects)")
    
    def add_suspect(self, fingerprint_id, name, age, description, image_path=None):
        """
        Add or update suspect information
        
        Args:
            fingerprint_id: ID number used in fingerprint sensor
            name: Suspect's name
            age: Suspect's age
            description: Additional information
            image_path: Path to suspect's photo (optional)
        """
        suspect_data = {
            'fingerprint_id': fingerprint_id,
            'name': name,
            'age': age,
            'description': description,
            'image_path': image_path,
            'created_at': datetime.now().isoformat(),
            'last_matched': None
        }
        
        self.suspects_db[str(fingerprint_id)] = suspect_data
        self.save_database()
        print(f"✓ Added suspect: {name} (ID: {fingerprint_id})")
    
    def get_suspect(self, fingerprint_id):
        """Get suspect information by fingerprint ID"""
        return self.suspects_db.get(str(fingerprint_id))
    
    def display_suspect(self, fingerprint_id, confidence=0):
        """
        Display suspect information when a match is found
        
        Args:
            fingerprint_id: Matched fingerprint ID
            confidence: Match confidence score
        """
        suspect = self.get_suspect(fingerprint_id)
        
        if suspect:
            print("\n" + "="*60)
            print("🔍 MATCH FOUND!")
            print("="*60)
            print(f"Fingerprint ID:  {fingerprint_id}")
            print(f"Confidence:      {confidence}")
            print(f"Name:            {suspect['name']}")
            print(f"Age:             {suspect['age']}")
            print(f"Description:     {suspect['description']}")
            print(f"Registered:      {suspect['created_at']}")
            
            if suspect.get('image_path') and os.path.exists(suspect['image_path']):
                print(f"Photo:           {suspect['image_path']}")
                print("\n[Opening suspect photo...]")
                self.open_image(suspect['image_path'])
            else:
                print("Photo:           Not available")
            
            # Update last matched time
            suspect['last_matched'] = datetime.now().isoformat()
            self.save_database()
            
            print("="*60 + "\n")
        else:
            print(f"\n⚠ Match found (ID: {fingerprint_id}), but no suspect data available!")
            print("   Use 'add' command to register this suspect.\n")
    
    def open_image(self, image_path):
        """Open image file using system default viewer"""
        system = platform.system()
        
        try:
            if system == 'Darwin':  # macOS
                subprocess.run(['open', image_path], check=False)
            elif system == 'Windows':
                subprocess.run(['cmd', '/c', 'start', '', image_path], check=False, shell=True)
            else:  # Linux and others
                subprocess.run(['xdg-open', image_path], check=False)
        except Exception as e:
            print(f"  Could not open image: {e}")
    
    def enroll_fingerprint(self, fingerprint_id):
        """Enroll a new fingerprint"""
        print(f"\n📝 Enrolling fingerprint ID: {fingerprint_id}")
        print("Follow the instructions from Arduino...")
        
        self.send_command(f"ENROLL:{fingerprint_id}")
        responses = self.read_response(timeout=60)
        
        # Check if enrollment was successful
        for response in responses:
            if 'ENROLL_SUCCESS' in response:
                return True
        return False
    
    def scan_fingerprint(self):
        """Scan and match fingerprint"""
        print("\n🔍 Scanning fingerprint...")
        print("Place finger on sensor...")
        
        self.send_command("SCAN")
        responses = self.read_response(timeout=30)
        
        # Parse response
        for response in responses:
            if 'MATCH_FOUND:' in response:
                parts = response.split(':')
                if len(parts) >= 3:
                    fingerprint_id = int(parts[1])
                    confidence = int(parts[2])
                    self.display_suspect(fingerprint_id, confidence)
                    return fingerprint_id
            elif 'MATCH_NOTFOUND' in response:
                print("\n⚠ No match found in database\n")
                return None
        
        return None
    
    def get_template_count(self):
        """Get number of stored fingerprints"""
        self.send_command("COUNT")
        responses = self.read_response(timeout=5)
        
        for response in responses:
            if 'COUNT:' in response:
                count = int(response.split(':')[1])
                print(f"\n📊 Fingerprints stored: {count}\n")
                return count
        return 0
    
    def delete_fingerprint(self, fingerprint_id):
        """Delete a fingerprint from sensor"""
        print(f"\n🗑️  Deleting fingerprint ID: {fingerprint_id}")
        
        self.send_command(f"DELETE:{fingerprint_id}")
        responses = self.read_response(timeout=10)
        
        for response in responses:
            if 'DELETE_SUCCESS' in response:
                print(f"✓ Fingerprint {fingerprint_id} deleted from sensor")
                
                # Also remove from database
                if str(fingerprint_id) in self.suspects_db:
                    del self.suspects_db[str(fingerprint_id)]
                    self.save_database()
                    print(f"✓ Suspect data removed from database")
                return True
        return False
    
    def list_suspects(self):
        """List all suspects in database"""
        if not self.suspects_db:
            print("\nℹ No suspects in database\n")
            return
        
        print("\n" + "="*60)
        print("📋 SUSPECTS DATABASE")
        print("="*60)
        for fid, suspect in sorted(self.suspects_db.items(), key=lambda x: int(x[0])):
            print(f"\nID {fid}:")
            print(f"  Name:        {suspect['name']}")
            print(f"  Age:         {suspect['age']}")
            print(f"  Description: {suspect['description']}")
            print(f"  Registered:  {suspect['created_at']}")
            if suspect.get('last_matched'):
                print(f"  Last Match:  {suspect['last_matched']}")
        print("="*60 + "\n")
    
    def interactive_mode(self):
        """Run interactive command-line interface"""
        print("\n" + "="*60)
        print("🔐 FINGERPRINT AUTOMATION SYSTEM")
        print("="*60)
        
        if not self.connect():
            return
        
        self.print_help()
        
        try:
            while True:
                command = input("\n> ").strip().lower()
                
                if command == 'scan' or command == 's':
                    self.scan_fingerprint()
                
                elif command.startswith('enroll') or command.startswith('e'):
                    parts = command.split()
                    if len(parts) >= 2:
                        try:
                            fid = int(parts[1])
                            if self.enroll_fingerprint(fid):
                                # Prompt for suspect information
                                print("\n📝 Enter suspect information:")
                                name = input("  Name: ").strip()
                                age = input("  Age: ").strip()
                                description = input("  Description: ").strip()
                                image = input("  Image path (optional, press Enter to skip): ").strip()
                                
                                if image and not os.path.exists(image):
                                    print(f"  ⚠ Warning: Image file not found: {image}")
                                    image = None
                                
                                self.add_suspect(fid, name, age, description, image)
                        except ValueError:
                            print("  ✗ Invalid ID number")
                    else:
                        print("  Usage: enroll <ID>")
                
                elif command.startswith('add'):
                    parts = command.split()
                    if len(parts) >= 2:
                        try:
                            fid = int(parts[1])
                            print(f"\n📝 Adding suspect information for ID {fid}:")
                            name = input("  Name: ").strip()
                            age = input("  Age: ").strip()
                            description = input("  Description: ").strip()
                            image = input("  Image path (optional, press Enter to skip): ").strip()
                            
                            if image and not os.path.exists(image):
                                print(f"  ⚠ Warning: Image file not found: {image}")
                                image = None
                            
                            self.add_suspect(fid, name, age, description, image)
                        except ValueError:
                            print("  ✗ Invalid ID number")
                    else:
                        print("  Usage: add <ID>")
                
                elif command == 'list' or command == 'l':
                    self.list_suspects()
                
                elif command == 'count' or command == 'c':
                    self.get_template_count()
                
                elif command.startswith('delete') or command.startswith('d'):
                    parts = command.split()
                    if len(parts) >= 2:
                        try:
                            fid = int(parts[1])
                            self.delete_fingerprint(fid)
                        except ValueError:
                            print("  ✗ Invalid ID number")
                    else:
                        print("  Usage: delete <ID>")
                
                elif command == 'help' or command == 'h' or command == '?':
                    self.print_help()
                
                elif command == 'quit' or command == 'q' or command == 'exit':
                    print("\n👋 Goodbye!")
                    break
                
                else:
                    print(f"  ✗ Unknown command: {command}")
                    print("  Type 'help' for available commands")
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user")
        
        finally:
            self.disconnect()
    
    def print_help(self):
        """Print help message"""
        print("\n📖 AVAILABLE COMMANDS:")
        print("  scan (s)         - Scan fingerprint and display suspect info")
        print("  enroll <ID> (e)  - Enroll new fingerprint with ID")
        print("  add <ID>         - Add/update suspect information for ID")
        print("  list (l)         - List all suspects in database")
        print("  count (c)        - Show number of stored fingerprints")
        print("  delete <ID> (d)  - Delete fingerprint and suspect data")
        print("  help (h)         - Show this help message")
        print("  quit (q)         - Exit application")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Fingerprint Automation System')
    parser.add_argument('-p', '--port', default='/dev/ttyUSB0',
                        help='Serial port (default: /dev/ttyUSB0)')
    parser.add_argument('-b', '--baudrate', type=int, default=9600,
                        help='Baud rate (default: 9600)')
    
    args = parser.parse_args()
    
    app = FingerprintApp(port=args.port, baudrate=args.baudrate)
    app.interactive_mode()


if __name__ == '__main__':
    main()
