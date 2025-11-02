#!/usr/bin/env python3
"""
Web controller sederhana untuk mengontrol script autoFillForm.py melalui GitHub API
"""

import json
import os
import sys
from datetime import datetime

def create_control_file():
    """Buat file kontrol jika belum ada"""
    if not os.path.exists('control.json'):
        control_data = {
            "status": "running",
            "last_updated": datetime.now().isoformat()
        }
        with open('control.json', 'w') as f:
            json.dump(control_data, f)
        print("File control.json telah dibuat dengan status 'running'")

def set_status(status):
    """Set status kontrol"""
    if not os.path.exists('control.json'):
        create_control_file()
    
    # Baca data kontrol yang ada
    with open('control.json', 'r') as f:
        control_data = json.load(f)
    
    # Update status
    control_data['status'] = status
    control_data['last_updated'] = datetime.now().isoformat()
    
    # Simpan kembali
    with open('control.json', 'w') as f:
        json.dump(control_data, f)
    
    print(f"Status kontrol telah diubah menjadi: {status}")

def get_status():
    """Dapatkan status kontrol"""
    if not os.path.exists('control.json'):
        create_control_file()
        return "running"
    
    with open('control.json', 'r') as f:
        control_data = json.load(f)
    
    return control_data.get('status', 'running')

def main():
    if len(sys.argv) < 2:
        print("Penggunaan:")
        print("  python web_controller.py start    # Mulai script")
        print("  python web_controller.py stop     # Hentikan script")
        print("  python web_controller.py status   # Cek status")
        return 1
    
    command = sys.argv[1].lower()
    
    if command == 'start':
        set_status('running')
        print("Script akan mulai berjalan pada workflow berikutnya")
    elif command == 'stop':
        set_status('stopped')
        print("Script akan dihentikan pada workflow berikutnya")
    elif command == 'status':
        status = get_status()
        print(f"Status saat ini: {status}")
    else:
        print(f"Perintah tidak dikenali: {command}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())