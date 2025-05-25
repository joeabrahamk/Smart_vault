import tkinter as tk
from tkinter import filedialog, messagebox
from crypto_tools import generate_key, save_key, load_key, encrypt_file, decrypt_file
from usb_check import get_usb_serial, save_usb_serial, is_usb_authorized
import os

KEY_FILE = "vault.key"

def register_usb():
    serial = get_usb_serial()
    if not serial:
        messagebox.showerror("Error", "No USB drive found.")
        return
    save_usb_serial(serial)
    messagebox.showinfo("Success", f"USB Registered.\nSerial: {serial}")

def encrypt_gui():
    if not is_usb_authorized():
        messagebox.showerror("Access Denied", "Unauthorized USB device.")
        return

    file_path = filedialog.askopenfilename(title="Select file to encrypt")
    if not file_path:
        return

    if not os.path.exists(KEY_FILE):
        key = generate_key()
        save_key(key)
    else:
        key = load_key()

    encrypt_file(file_path, key)
    messagebox.showinfo("Success", f"File encrypted: {file_path}.enc")

def decrypt_gui():
    if not is_usb_authorized():
        messagebox.showerror("Access Denied", "Unauthorized USB device.")
        return

    file_path = filedialog.askopenfilename(title="Select .enc file to decrypt")
    if not file_path or not file_path.endswith(".enc"):
        return

    key = load_key()
    decrypt_file(file_path, key)
    messagebox.showinfo("Success", f"File decrypted: {file_path.replace('.enc', '')}")

def launch_gui():
    window = tk.Tk()
    window.title("Smart Vault 🔐")
    window.geometry("320x250")
    window.resizable(False, False)

    tk.Label(window, text="Smart Vault GUI", font=("Arial", 16, "bold")).pack(pady=10)

    tk.Button(window, text="🔑 Register USB Key", command=register_usb, width=25).pack(pady=5)
    tk.Button(window, text="🛡️ Encrypt File", command=encrypt_gui, width=25).pack(pady=5)
    tk.Button(window, text="🔓 Decrypt File", command=decrypt_gui, width=25).pack(pady=5)

    tk.Label(window, text="(USB key required for secure access)", font=("Arial", 9)).pack(pady=15)
    tk.Label(window, text="© 2025 Smart Vault", font=("Arial", 8)).pack(side=tk.BOTTOM, pady=5)
    tk.Label(window, text="Developed by github.com/joeabrahamk", font=("Arial", 8)).pack(side=tk.BOTTOM)
    window.mainloop()

if __name__ == "__main__":
    launch_gui()
