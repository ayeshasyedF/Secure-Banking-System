import hashlib
from database_handler import find_user


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def authenticate_user(username, password):
    user = find_user(username)

    if user is None:
        return False

    entered_hash = hash_password(password)

    if user["password"] == entered_hash:
        return True

    return False