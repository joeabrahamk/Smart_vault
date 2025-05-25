from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def save_key(key, filename="vault.key"):
    with open(filename, 'wb') as f:
        f.write(key)

def load_key(filename="vault.key"):
    with open(filename, 'rb') as f:
        return f.read()

def encrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        data = f.read()

    encrypted = Fernet(key).encrypt(data)

    with open(file_path + ".enc", 'wb') as f:
        f.write(encrypted)

def decrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        encrypted = f.read()

    decrypted = Fernet(key).decrypt(encrypted)

    original_path = file_path.replace(".enc", "")
    with open(original_path, 'wb') as f:
        f.write(decrypted)
