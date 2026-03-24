from datetime import datetime
import os

from crypto.aes_utils import encrypt_message, decrypt_message

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_FILE = os.path.join(PROJECT_ROOT, "logs", "audit_log.txt")
AUDIT_KEY = "BANK_AUDIT_SECRET_2026"


def write_log(username, action, details=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{timestamp} | {username} | {action} | {details}"

    encrypted_line = encrypt_message(log_line, AUDIT_KEY)

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(encrypted_line + "\n")


def read_decrypted_logs():
    decrypted_logs = []

    if not os.path.exists(LOG_FILE):
        return decrypted_logs

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            try:
                decrypted_line = decrypt_message(line, AUDIT_KEY)
                decrypted_logs.append(decrypted_line)
            except Exception:
                decrypted_logs.append("[Could not decrypt one log entry]")

    return decrypted_logs