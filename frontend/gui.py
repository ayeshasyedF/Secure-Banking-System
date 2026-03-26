import json
import os
import socket
import tkinter as tk
from tkinter import messagebox

from backend.auth import hash_password, verify_server_auth, derive_master_secret
from crypto.hmac_utils import generate_hmac
from crypto.kdf_utils import derive_keys
from crypto.crypto_utils import secure_send, secure_receive, send_packet, receive_packet

HOST = "127.0.0.1"
PORT = 5000


class BankingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Banking ATM")
        self.root.geometry("500x500")

        self.client_socket = None
        self.encryption_key = None
        self.mac_key = None
        self.username = None

        self.build_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def build_login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Secure Banking ATM", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, width=30, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Login", width=20, command=self.login).pack(pady=20)

        self.status_label = tk.Label(self.root, text="", fg="blue")
        self.status_label.pack()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

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
                raise Exception("Server closed connection.")

            packet_2 = json.loads(packet_text)

            if packet_2.get("type") == "KEY_EXCHANGE_ERROR":
                raise Exception(packet_2.get("message"))

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
                raise Exception("Server authentication failed.")

            master_secret = derive_master_secret(auth_key, client_nonce, server_nonce)
            self.encryption_key, self.mac_key = derive_keys(master_secret)

            login_reply, error = secure_receive(
                self.client_socket,
                self.encryption_key,
                self.mac_key,
                "CLIENT"
            )

            if error is not None or login_reply != "LOGIN_SUCCESS":
                raise Exception("Login failed.")

            self.username = username
            self.build_main_screen()

        except Exception as e:
            messagebox.showerror("Login Error", str(e))
            if self.client_socket:
                self.client_socket.close()
                self.client_socket = None

    def build_main_screen(self):
        self.clear_screen()

        tk.Label(self.root, text=f"Welcome, {self.username}", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Button(self.root, text="Check Balance", width=20, command=self.check_balance).pack(pady=5)

        tk.Label(self.root, text="Deposit Amount").pack()
        self.deposit_entry = tk.Entry(self.root, width=20)
        self.deposit_entry.pack()
        tk.Button(self.root, text="Deposit", width=20, command=self.deposit).pack(pady=5)

        tk.Label(self.root, text="Withdraw Amount").pack()
        self.withdraw_entry = tk.Entry(self.root, width=20)
        self.withdraw_entry.pack()
        tk.Button(self.root, text="Withdraw", width=20, command=self.withdraw).pack(pady=5)

        tk.Label(self.root, text="Transfer Username").pack()
        self.transfer_user_entry = tk.Entry(self.root, width=20)
        self.transfer_user_entry.pack()

        tk.Label(self.root, text="Transfer Amount").pack()
        self.transfer_amount_entry = tk.Entry(self.root, width=20)
        self.transfer_amount_entry.pack()
        tk.Button(self.root, text="Transfer", width=20, command=self.transfer).pack(pady=5)

        tk.Button(self.root, text="Exit", width=20, command=self.exit_session).pack(pady=10)

        self.output_box = tk.Text(self.root, height=8, width=55)
        self.output_box.pack(pady=10)

    def send_transaction(self, message):
        try:
            secure_send(self.client_socket, message, self.encryption_key, self.mac_key)

            reply, error = secure_receive(
                self.client_socket,
                self.encryption_key,
                self.mac_key,
                "CLIENT"
            )

            if error is not None:
                self.output_box.insert(tk.END, f"Error: {error}\n")
                return None

            return reply

        except Exception as e:
            self.output_box.insert(tk.END, f"Error: {str(e)}\n")
            return None

    def check_balance(self):
        reply = self.send_transaction("BALANCE")
        if reply:
            self.output_box.insert(tk.END, f"{reply}\n")

    def deposit(self):
        amount = self.deposit_entry.get().strip()
        reply = self.send_transaction(f"DEPOSIT,{amount}")
        if reply:
            self.output_box.insert(tk.END, f"{reply}\n")

    def withdraw(self):
        amount = self.withdraw_entry.get().strip()
        reply = self.send_transaction(f"WITHDRAW,{amount}")
        if reply:
            self.output_box.insert(tk.END, f"{reply}\n")

    def transfer(self):
        user = self.transfer_user_entry.get().strip()
        amount = self.transfer_amount_entry.get().strip()
        reply = self.send_transaction(f"TRANSFER,{user},{amount}")
        if reply:
            self.output_box.insert(tk.END, f"{reply}\n")

    def exit_session(self):
        reply = self.send_transaction("EXIT")
        if reply:
            self.output_box.insert(tk.END, f"{reply}\n")

        if self.client_socket:
            self.client_socket.close()

        self.build_login_screen()


def main():
    root = tk.Tk()
    app = BankingGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()