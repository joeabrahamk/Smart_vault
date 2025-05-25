import os
import json
import subprocess
import platform

USB_CONFIG_FILE = "usb_config.json"

def get_usb_serials():
    serials = []
    if platform.system() == "Windows":
        result = subprocess.run(["wmic", "diskdrive", "get", "SerialNumber,MediaType"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if "Removable Media" in line:
                parts = line.strip().split()
                if len(parts) > 0:
                    serials.append(parts[0])
    return serials

# ✅ ADD THIS FUNCTION for GUI to use
def get_usb_serial():
    serials = get_usb_serials()
    return serials[0] if serials else None

def save_usb_serial(serial):
    with open(USB_CONFIG_FILE, 'w') as f:
        json.dump({"serial": serial}, f)

def load_usb_serial():
    if not os.path.exists(USB_CONFIG_FILE):
        return None
    with open(USB_CONFIG_FILE, 'r') as f:
        return json.load(f).get("serial")

def is_usb_authorized():
    saved = load_usb_serial()
    current = get_usb_serial()
    return saved == current
