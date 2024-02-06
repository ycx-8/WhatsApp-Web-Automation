from cryptography.fernet import Fernet
# from const import CONTACT_PATH_LOCAL

def encrypt_json(path: str):
    """To encrypt contacts.json stored in local directory

    Args:
        path (str): The path to contacts.json
    """
    key = Fernet.generate_key()
    with open("filekey.key", "wb") as f:
        f.write(key)
    with open("filekey.key", "rb") as f:
        key = f.read()
    fernet = Fernet(key)
    with open(path, "rb") as f:
        original = f.read()
    encrypted = fernet.encrypt(original)
    with open(path, "wb") as f:
        f.write(encrypted)


def decrypt_json(path: str):
    """To decrypt contacts.json stored in local directory

    Args:
        path (str): The path to contacts.json
    """
    with open("filekey.key", "rb") as f:
        key = f.read()
    fernet = Fernet(key)
    with open(path, "rb") as f:
        encrypted = f.read()
    decrypted = fernet.decrypt(encrypted)
    with open(path, "wb") as f:
        f.write(decrypted)
        

def is_encrypted(path):
    """Check if contacts.json is encrypted or not

    Args:
        path (str): The path to contacts.json

    Returns:
        bool: returns True if encrypted, otherwise False
    """
    try:
        decrypt_json(path)
        encrypt_json(path)
        return True
    except Exception as e:
        return False


# ----- Below for testing -----
# print(is_encrypted(PATH))