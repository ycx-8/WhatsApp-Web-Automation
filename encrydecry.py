from cryptography.fernet import Fernet

ALT_PATH = "resources/contacts_encrypt.json"

def encrypt_json():
    key = Fernet.generate_key()
    with open("filekey.key", "wb") as f:
        f.write(key)
    with open("filekey.key", "rb") as f:
        key = f.read()
    fernet = Fernet(key)
    with open(ALT_PATH, "rb") as f:
        original = f.read()
    encrypted = fernet.encrypt(original)
    with open(ALT_PATH, "wb") as f:
        f.write(encrypted)

def decrypt_json():
    with open("filekey.key", "rb") as f:
        key = f.read()
    fernet = Fernet(key)
    with open(ALT_PATH, "rb") as f:
        encrypted = f.read()
    decrypted = fernet.decrypt(encrypted)
    with open(ALT_PATH, "wb") as f:
        f.write(decrypted)