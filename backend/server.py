import json
import socket
import threading

from backend.auth import (
    verify_client_auth,
    create_server_auth_response,
    derive_master_secret,
)
from backend.transaction import handle_transaction
from backend.audit import write_log
from crypto.kdf_utils import derive_keys
from crypto.crypto_utils import secure_send, secure_receive, send_packet, receive_packet

HOST = "127.0.0.1"
PORT = 5000


def handle_client(client_socket, client_address):
    print(f"Connected by {client_address}")
    logged_in_user = None

    try:
        # -------------------------------
        # Message 1: client -> server
        # username, client_nonce, HMAC
        # -------------------------------
        packet_text = receive_packet(client_socket)

        if packet_text is None:
            client_socket.close()
            return

        try:
            packet = json.loads(packet_text)
        except json.JSONDecodeError:
            send_packet(client_socket, json.dumps({
                "type": "KEY_EXCHANGE_ERROR",
                "message": "INVALID_PACKET"
            }))
            client_socket.close()
            return

        if packet.get("type") != "KEY_EXCHANGE_1":
            send_packet(client_socket, json.dumps({
                "type": "KEY_EXCHANGE_ERROR",
                "message": "INVALID_PROTOCOL_STEP"
            }))
            client_socket.close()
            return

        username = packet.get("username")
        client_nonce = packet.get("client_nonce")
        received_hmac = packet.get("hmac")

        print("\n=== AUTHENTICATED KEY DISTRIBUTION PROTOCOL ===")
        print("Message 1 received from client")
        print("Username:", username)
        print("Client Nonce (Nc):", client_nonce)
        print("Received HMAC:", received_hmac)

        valid_client, auth_key = verify_client_auth(username, client_nonce, received_hmac)

        if not valid_client:
            print("Client authentication: FAILED")
            send_packet(client_socket, json.dumps({
                "type": "KEY_EXCHANGE_ERROR",
                "message": "CLIENT_AUTH_FAILED"
            }))
            write_log("UNKNOWN", "LOGIN_FAILED", "Client authentication failed")
            client_socket.close()
            return

        print("Client authentication: PASSED")

        # -------------------------------
        # Message 2: server -> client
        # server_nonce, HMAC
        # -------------------------------
        server_nonce, server_hmac = create_server_auth_response(username, client_nonce, auth_key)

        response_packet = {
            "type": "KEY_EXCHANGE_2",
            "server_nonce": server_nonce,
            "hmac": server_hmac
        }

        print("\nMessage 2 sent to client")
        print("Server Nonce (Ns):", server_nonce)
        print("Server HMAC:", server_hmac)

        send_packet(client_socket, json.dumps(response_packet))

        # -------------------------------
        # Derive Master Secret and session keys
        # -------------------------------
        master_secret = derive_master_secret(auth_key, client_nonce, server_nonce)
        encryption_key, mac_key = derive_keys(master_secret)

        print("\n=== SESSION KEY DERIVATION ===")
        print("Master Secret:", master_secret)
        print("Encryption Key:", encryption_key)
        print("MAC Key:", mac_key)
        print("================================\n")

        logged_in_user = username
        write_log(username, "LOGIN_SUCCESS", "Authenticated key distribution completed")

        # Optional secure confirmation after successful protocol
        secure_send(client_socket, "LOGIN_SUCCESS", encryption_key, mac_key)

        # -------------------------------
        # Secure transaction phase
        # -------------------------------
        while True:
            transaction_message, error = secure_receive(
                client_socket,
                encryption_key,
                mac_key,
                "SERVER"
            )

            if error == "NO_DATA":
                break

            if error is not None:
                print("Secure receive error during transaction:", error)
                write_log(logged_in_user, "SECURE_RECEIVE_FAILED", error)
                secure_send(client_socket, "ERROR,SECURE_COMMUNICATION_FAILED", encryption_key, mac_key)
                break

            print("Client sent secure transaction:", transaction_message)

            transaction_response = handle_transaction(logged_in_user, transaction_message)
            secure_send(client_socket, transaction_response, encryption_key, mac_key)

            if transaction_response == "GOODBYE":
                break

    except Exception as error:
        print("Server error:", error)

        if logged_in_user is not None:
            write_log(logged_in_user, "SERVER_ERROR", str(error))
        else:
            write_log("UNKNOWN", "SERVER_ERROR", str(error))

    finally:
        client_socket.close()
        print(f"Connection with {client_address} closed")


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        # Create a new thread for each client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()


if __name__ == "__main__":
    main()