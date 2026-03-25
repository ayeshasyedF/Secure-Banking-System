import hashlib
import os

from backend.database_handler import find_user
from crypto.hmac_utils import generate_hmac, verify_hmac


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def get_stored_auth_key(username):
    user = find_user(username)

    if user is None:
        return None

    return user["password"]


def verify_client_auth(username, client_nonce, received_hmac):
    auth_key = get_stored_auth_key(username)

    if auth_key is None:
        return False, None

    message = f"{username}|{client_nonce}"

    if not verify_hmac(message, auth_key, received_hmac):
        return False, None

    return True, auth_key


def create_server_auth_response(username, client_nonce, auth_key):
    server_nonce = os.urandom(16).hex()
    message = f"{username}|{client_nonce}|{server_nonce}|SERVER"
    server_hmac = generate_hmac(message, auth_key)

    return server_nonce, server_hmac


def verify_server_auth(username, client_nonce, server_nonce, received_hmac, auth_key):
    message = f"{username}|{client_nonce}|{server_nonce}|SERVER"
    return verify_hmac(message, auth_key, received_hmac)


def derive_master_secret(auth_key, client_nonce, server_nonce):
    material = f"{auth_key}|{client_nonce}|{server_nonce}|MASTER"
    return hashlib.sha256(material.encode("utf-8")).hexdigest()