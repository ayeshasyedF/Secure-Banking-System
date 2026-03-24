import socket
from auth import authenticate_user
from transaction import handle_transaction
from audit import write_log

HOST = "127.0.0.1"
PORT = 5000


def handle_client(client_socket, client_address):
    print(f"Connected by {client_address}")
    logged_in_user = None

    try:
        login_message = client_socket.recv(1024).decode()

        if not login_message:
            client_socket.close()
            return

        print("Client sent login:", login_message)

        parts = login_message.split(",")

        if len(parts) != 2:
            response = "INVALID_FORMAT"
            client_socket.send(response.encode())
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

        client_socket.send(response.encode())

        if logged_in_user is None:
            client_socket.close()
            return

        while True:
            transaction_message = client_socket.recv(1024).decode()

            if not transaction_message:
                break

            print("Client sent transaction:", transaction_message)

            transaction_response = handle_transaction(logged_in_user, transaction_message)
            client_socket.send(transaction_response.encode())

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