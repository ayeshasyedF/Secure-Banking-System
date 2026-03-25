import json
import os
import socket

from backend.auth import hash_password, verify_server_auth, derive_master_secret
from crypto.hmac_utils import generate_hmac
from crypto.kdf_utils import derive_keys
from crypto.crypto_utils import secure_send, secure_receive, send_packet, receive_packet

HOST = "127.0.0.1"
PORT = 5000


def print_menu():
    print("\nChoose an option:")
    print("1. Check Balance")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Transfer Money")
    print("5. Exit")


def format_server_reply(reply):
    parts = reply.split(",")

    if parts[0] == "BALANCE":
        return f"Your current balance is: ${parts[1]}"

    elif parts[0] == "DEPOSIT_SUCCESS":
        return f"Deposit successful. New balance: ${parts[1]}"

    elif parts[0] == "WITHDRAW_SUCCESS":
        return f"Withdrawal successful. New balance: ${parts[1]}"

    elif parts[0] == "TRANSFER_SUCCESS":
        return f"Transfer successful. New balance: ${parts[1]}"

    elif parts[0] == "LOGIN_SUCCESS":
        return "Login successful."

    elif parts[0] == "LOGIN_FAILED":
        return "Login failed. Please check your username or password."

    elif parts[0] == "INVALID_FORMAT":
        return "Invalid message format."

    elif parts[0] == "ERROR":
        if len(parts) > 1:
            if parts[1] == "INSUFFICIENT_FUNDS":
                return "Transaction failed: insufficient funds."
            elif parts[1] == "INVALID_AMOUNT":
                return "Transaction failed: invalid amount."
            elif parts[1] == "RECEIVER_NOT_FOUND":
                return "Transaction failed: receiver not found."
            elif parts[1] == "INVALID_DEPOSIT_FORMAT":
                return "Deposit failed: invalid format."
            elif parts[1] == "INVALID_WITHDRAW_FORMAT":
                return "Withdrawal failed: invalid format."
            elif parts[1] == "INVALID_TRANSFER_FORMAT":
                return "Transfer failed: invalid format."
            elif parts[1] == "UNKNOWN_COMMAND":
                return "Unknown command."
            elif parts[1] == "SECURE_COMMUNICATION_FAILED":
                return "Secure communication failed."
        return "An error occurred."

    elif parts[0] == "GOODBYE":
        return "Session ended. Goodbye."

    return reply


def main():
    username = input("Enter username: ")
    password = input("Enter password: ")

    auth_key = hash_password(password)
    client_nonce = os.urandom(16).hex()

    message_1 = f"{username}|{client_nonce}"
    client_hmac = generate_hmac(message_1, auth_key)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # -------------------------------
    # Message 1: client -> server
    # -------------------------------
    packet_1 = {
        "type": "KEY_EXCHANGE_1",
        "username": username,
        "client_nonce": client_nonce,
        "hmac": client_hmac
    }

    send_packet(client_socket, json.dumps(packet_1))

    # -------------------------------
    # Message 2: server -> client
    # -------------------------------
    packet_text = receive_packet(client_socket)

    if packet_text is None:
        print("Server closed the connection.")
        client_socket.close()
        return

    try:
        packet_2 = json.loads(packet_text)
    except json.JSONDecodeError:
        print("Invalid response from server.")
        client_socket.close()
        return

    if packet_2.get("type") == "KEY_EXCHANGE_ERROR":
        print("Key exchange failed:", packet_2.get("message"))
        client_socket.close()
        return

    if packet_2.get("type") != "KEY_EXCHANGE_2":
        print("Unexpected protocol response.")
        client_socket.close()
        return

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
        print("Server authentication failed.")
        client_socket.close()
        return

    # -------------------------------
    # Derive Master Secret and session keys
    # -------------------------------
    master_secret = derive_master_secret(auth_key, client_nonce, server_nonce)
    encryption_key, mac_key = derive_keys(master_secret)

    # Secure confirmation
    login_reply, error = secure_receive(
        client_socket,
        encryption_key,
        mac_key,
        "CLIENT"
    )

    if error is not None:
        print("Could not securely receive server reply:", error)
        client_socket.close()
        return

    print(format_server_reply(login_reply))

    if login_reply != "LOGIN_SUCCESS":
        client_socket.close()
        return

    while True:
        print_menu()
        choice = input("Enter choice: ")

        if choice == "1":
            transaction_message = "BALANCE"
        elif choice == "2":
            amount = input("Enter amount to deposit: ")
            transaction_message = f"DEPOSIT,{amount}"
        elif choice == "3":
            amount = input("Enter amount to withdraw: ")
            transaction_message = f"WITHDRAW,{amount}"
        elif choice == "4":
            receiver = input("Enter receiver username: ")
            amount = input("Enter amount to transfer: ")
            transaction_message = f"TRANSFER,{receiver},{amount}"
        elif choice == "5":
            transaction_message = "EXIT"
        else:
            print("Invalid choice. Try again.")
            continue

        secure_send(client_socket, transaction_message, encryption_key, mac_key)

        transaction_reply, error = secure_receive(
            client_socket,
            encryption_key,
            mac_key,
            "CLIENT"
        )

        if error is not None:
            print("Could not securely receive transaction reply:", error)
            break

        print(format_server_reply(transaction_reply))

        if transaction_reply == "GOODBYE":
            break

    client_socket.close()


if __name__ == "__main__":
    main()