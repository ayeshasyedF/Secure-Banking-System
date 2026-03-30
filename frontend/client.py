import json
import os
import socket

from backend.auth import hash_password, verify_server_auth, derive_master_secret
from backend.database_handler import load_data, save_data, find_user
from crypto.hmac_utils import generate_hmac
from crypto.kdf_utils import derive_keys
from crypto.crypto_utils import secure_send, secure_receive, send_packet, receive_packet

HOST = "127.0.0.1"
PORT = 5000


class BankingClient:
    def __init__(self):
        self.client_socket = None
        self.encryption_key = None
        self.mac_key = None
        self.username = None

    # ---------------------------
    # REGISTER
    # ---------------------------
    def register(self, username, password):
        """
        Register a new user by writing directly to the database.
        Stores the password as sha256(password) — same hash login uses.
        """
        try:
            if find_user(username):
                return False, "Username already exists."

            hashed = hash_password(password)
            data = load_data()
            data["users"].append({
                "username": username,
                "password": hashed,
                "balance": 0.0
            })
            save_data(data)
            return True, "Registration successful."
        except Exception as e:
            return False, str(e)

    # ---------------------------
    # LOGIN
    # ---------------------------
    def login(self, username, password):
        try:
            auth_key = hash_password(password)
            client_nonce = os.urandom(16).hex()

            message_1 = f"{username}|{client_nonce}"
            client_hmac = generate_hmac(message_1, auth_key)

            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((HOST, PORT))

            packet_1 = {
                "type": "KEY_EXCHANGE_1",
                "username": username,
                "client_nonce": client_nonce,
                "hmac": client_hmac
            }

            send_packet(self.client_socket, json.dumps(packet_1))

            packet_text = receive_packet(self.client_socket)
            if packet_text is None:
                return False, "Server closed connection."

            packet_2 = json.loads(packet_text)

            if packet_2.get("type") == "KEY_EXCHANGE_ERROR":
                return False, packet_2.get("message")

            server_nonce = packet_2.get("server_nonce")
            server_hmac = packet_2.get("hmac")

            valid_server = verify_server_auth(
                username,
                client_nonce,
                server_nonce,
                server_hmac,
                auth_key
            )

            if not valid_server:
                return False, "Server authentication failed."

            master_secret = derive_master_secret(auth_key, client_nonce, server_nonce)
            self.encryption_key, self.mac_key = derive_keys(master_secret)

            login_reply, error = secure_receive(
                self.client_socket,
                self.encryption_key,
                self.mac_key,
                "CLIENT"
            )

            if error is not None or login_reply != "LOGIN_SUCCESS":
                return False, "Login failed."

            self.username = username
            return True, "Login successful."

        except Exception as e:
            return False, str(e)

    # ---------------------------
    # SEND TRANSACTION
    # ---------------------------
    def send(self, message):
        try:
            secure_send(self.client_socket, message, self.encryption_key, self.mac_key)

            reply, error = secure_receive(
                self.client_socket,
                self.encryption_key,
                self.mac_key,
                "CLIENT"
            )

            if error:
                return False, error

            return True, reply

        except Exception as e:
            return False, str(e)

    # ---------------------------
    # ACTIONS
    # ---------------------------
    def deposit(self, amount):
        return self.send(f"DEPOSIT,{amount}")

    def withdraw(self, amount):
        return self.send(f"WITHDRAW,{amount}")

    def check_balance(self):
        return self.send("BALANCE")

    def exit(self):
        result = self.send("EXIT")
        if self.client_socket:
            self.client_socket.close()
        return result