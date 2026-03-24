from backend.database_handler import (
    get_balance,
    deposit_money,
    withdraw_money,
    transfer_money,
)
from backend.audit import write_log


def handle_transaction(username, message):
    parts = message.split(",")
    command = parts[0].upper()

    if command == "BALANCE":
        balance = get_balance(username)
        write_log(username, "BALANCE_CHECK", f"Balance = {balance}")
        return f"BALANCE,{balance}"

    elif command == "DEPOSIT":
        if len(parts) != 2:
            write_log(username, "DEPOSIT_FAILED", "Invalid deposit format")
            return "ERROR,INVALID_DEPOSIT_FORMAT"

        try:
            amount = float(parts[1])
        except ValueError:
            write_log(username, "DEPOSIT_FAILED", "Amount was not a number")
            return "ERROR,INVALID_AMOUNT"

        if amount <= 0:
            write_log(username, "DEPOSIT_FAILED", "Amount must be greater than zero")
            return "ERROR,INVALID_AMOUNT"

        new_balance = deposit_money(username, amount)
        write_log(username, "DEPOSIT_SUCCESS", f"Deposited {amount}, New balance = {new_balance}")
        return f"DEPOSIT_SUCCESS,{new_balance}"

    elif command == "WITHDRAW":
        if len(parts) != 2:
            write_log(username, "WITHDRAW_FAILED", "Invalid withdraw format")
            return "ERROR,INVALID_WITHDRAW_FORMAT"

        try:
            amount = float(parts[1])
        except ValueError:
            write_log(username, "WITHDRAW_FAILED", "Amount was not a number")
            return "ERROR,INVALID_AMOUNT"

        if amount <= 0:
            write_log(username, "WITHDRAW_FAILED", "Amount must be greater than zero")
            return "ERROR,INVALID_AMOUNT"

        result = withdraw_money(username, amount)

        if result == "INSUFFICIENT_FUNDS":
            write_log(username, "WITHDRAW_FAILED", f"Tried to withdraw {amount}, insufficient funds")
            return "ERROR,INSUFFICIENT_FUNDS"

        write_log(username, "WITHDRAW_SUCCESS", f"Withdrew {amount}, New balance = {result}")
        return f"WITHDRAW_SUCCESS,{result}"

    elif command == "TRANSFER":
        if len(parts) != 3:
            write_log(username, "TRANSFER_FAILED", "Invalid transfer format")
            return "ERROR,INVALID_TRANSFER_FORMAT"

        receiver_username = parts[1]

        try:
            amount = float(parts[2])
        except ValueError:
            write_log(username, "TRANSFER_FAILED", "Amount was not a number")
            return "ERROR,INVALID_AMOUNT"

        if amount <= 0:
            write_log(username, "TRANSFER_FAILED", "Amount must be greater than zero")
            return "ERROR,INVALID_AMOUNT"

        result = transfer_money(username, receiver_username, amount)

        if result == "RECEIVER_NOT_FOUND":
            write_log(username, "TRANSFER_FAILED", f"Receiver {receiver_username} not found")
            return "ERROR,RECEIVER_NOT_FOUND"

        if result == "INSUFFICIENT_FUNDS":
            write_log(username, "TRANSFER_FAILED", f"Tried to transfer {amount} to {receiver_username}, insufficient funds")
            return "ERROR,INSUFFICIENT_FUNDS"

        write_log(username, "TRANSFER_SUCCESS", f"Transferred {amount} to {receiver_username}, New balance = {result}")
        return f"TRANSFER_SUCCESS,{result}"

    elif command == "EXIT":
        write_log(username, "SESSION_ENDED", "Client chose to exit")
        return "GOODBYE"

    else:
        write_log(username, "UNKNOWN_COMMAND", message)
        return "ERROR,UNKNOWN_COMMAND"