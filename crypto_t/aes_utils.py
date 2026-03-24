import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def format_aes_key(key_text):
    return hashlib.sha256(key_text.encode()).digest()


def encrypt_message(message, key_text):
    key = format_aes_key(key_text)
    iv = get_random_bytes(16)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))

    encrypted_data = iv + ciphertext
    return base64.b64encode(encrypted_data).decode()


def decrypt_message(encrypted_text, key_text):
    key = format_aes_key(key_text)

    encrypted_data = base64.b64decode(encrypted_text.encode())
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    return plaintext.decode()