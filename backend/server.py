import socket

from backend.auth import authenticate_user
from backend.transaction import handle_transaction
from backend.audit import write_log
from crypto.kdf_utils import derive_keys
from crypto.crypto_utils import secure_send, secure_receive

HOST = "127.0.0.1"
PORT = 5000

MASTER_SECRET = "SECURE_BANKING_MASTER_SECRET_2026"
ENCRYPTION_KEY, MAC_KEY = derive_keys(MASTER_SECRET)

print("\n=== KEY DERIVATION ===")
print("Master Secret:", MASTER_SECRET)
print("Encryption Key:", ENCRYPTION_KEY)
print("MAC Key:", MAC_KEY)
print("======================\n")


def handle_client(client_socket, client_address):
    print(f"Connected by {client_address}")
    logged_in_user = None

    try:
        login_message, error = secure_receive(
            client_socket,
            ENCRYPTION_KEY,
            MAC_KEY,
            "SERVER"
        )

        if error is not None:
            print("Secure receive error during login:", error)
            write_log("UNKNOWN", "LOGIN_FAILED", f"Secure receive error: {error}")
            secure_send(client_socket, "ERROR,SECURE_COMMUNICATION_FAILED", ENCRYPTION_KEY, MAC_KEY)
            client_socket.close()
            return

        print("Client sent secure login:", login_message)

        parts = login_message.split(",")

        if len(parts) != 2:
            secure_send(client_socket, "INVALID_FORMAT", ENCRYPTION_KEY, MAC_KEY)
            write_log("UNKNOWN", "LOGIN_FAILED", "Invalid login format")
            client_socket.close()
            return

        username = parts[0]
        password = parts[1]

        if authenticate_user(username, password):
            logged_in_user = username
            response = "LOGIN_SUCCESS"
            write_log(username, "LOGIN_SUCCESS")
        else:
            response = "LOGIN_FAILED"
            write_log(username, "LOGIN_FAILED", "Wrong username or password")

        secure_send(client_socket, response, ENCRYPTION_KEY, MAC_KEY)

        if logged_in_user is None:
            client_socket.close()
            return

        while True:
            transaction_message, error = secure_receive(
                client_socket,
                ENCRYPTION_KEY,
                MAC_KEY,
                "SERVER"
            )

            if error == "NO_DATA":
                break

            if error is not None:
                print("Secure receive error during transaction:", error)
                write_log(logged_in_user, "SECURE_RECEIVE_FAILED", error)
                secure_send(client_socket, "ERROR,SECURE_COMMUNICATION_FAILED", ENCRYPTION_KEY, MAC_KEY)
                break

            print("Client sent secure transaction:", transaction_message)

            transaction_response = handle_transaction(logged_in_user, transaction_message)
            secure_send(client_socket, transaction_response, ENCRYPTION_KEY, MAC_KEY)

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
        handle_client(client_socket, client_address)


if __name__ == "__main__":
    main()