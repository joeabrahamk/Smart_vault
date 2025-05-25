import os
import logging
from crypto_tools import generate_key, save_key, load_key, encrypt_file, decrypt_file
from usb_check import get_usb_serials, save_authorized_usb, is_usb_authorized

# Setup logging
logging.basicConfig(filename="activity_log.txt", level=logging.INFO, format="%(asctime)s %(message)s")

VAULT_PATH = "./vault/"
KEY_FILE = "vault.key"

def menu():
    print("\n==== SMART FILE VAULT ====")
    print("1. Register USB Key")
    print("2. Encrypt File")
    print("3. Decrypt File")
    print("4. Exit")

def register_usb():
    serials = get_usb_serials()
    if not serials:
        print("❌ No USB device found!")
        return
    save_authorized_usb(serials[0])
    print(f"✅ USB '{serials[0]}' registered as vault key.")

def encrypt():
    if not is_usb_authorized():
        print("🚫 Unauthorized USB. Access Denied.")
        return

    file = input("Enter full path of file to encrypt: ")
    if not os.path.exists(file):
        print("❌ File not found.")
        return

    if not os.path.exists(KEY_FILE):
        key = generate_key()
        save_key(key)
    else:
        key = load_key()

    encrypt_file(file, key)
    print("✅ File encrypted.")
    logging.info(f"Encrypted file: {file}")

def decrypt():
    if not is_usb_authorized():
        print("🚫 Unauthorized USB. Access Denied.")
        return

    file = input("Enter full path of .enc file to decrypt: ")
    if not os.path.exists(file):
        print("❌ File not found.")
        return

    key = load_key()
    decrypt_file(file, key)
    print("✅ File decrypted.")
    logging.info(f"Decrypted file: {file}")

if __name__ == "__main__":
    while True:
        menu()
        choice = input("Choose an option: ")
        if choice == "1":
            register_usb()
        elif choice == "2":
            encrypt()
        elif choice == "3":
            decrypt()
        elif choice == "4":
            break
        else:
            print("Invalid option.")
