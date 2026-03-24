import socket

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
        return "An error occurred."

    elif parts[0] == "GOODBYE":
        return "Session ended. Goodbye."

    return reply


def main():
    username = input("Enter username: ")
    password = input("Enter password: ")

    login_message = f"{username},{password}"

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    client_socket.send(login_message.encode())

    login_reply = client_socket.recv(1024).decode()

    if login_reply == "LOGIN_SUCCESS":
        print("Login successful.")
    elif login_reply == "LOGIN_FAILED":
        print("Login failed. Please check your username or password.")
        client_socket.close()
        return
    else:
        print("Invalid login format.")
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

        client_socket.send(transaction_message.encode())

        transaction_reply = client_socket.recv(1024).decode()
        print(format_server_reply(transaction_reply))

        if transaction_reply == "GOODBYE":
            break

    client_socket.close()


if __name__ == "__main__":
    main()