import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "Data", "database.json")


def load_data():
    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def find_user(username):
    data = load_data()

    for user in data["users"]:
        if user["username"] == username:
            return user

    return None


def get_balance(username):
    user = find_user(username)

    if user is not None:
        return user["balance"]

    return None


def deposit_money(username, amount):
    data = load_data()

    for user in data["users"]:
        if user["username"] == username:
            user["balance"] += amount
            save_data(data)
            return user["balance"]

    return None


def withdraw_money(username, amount):
    data = load_data()

    for user in data["users"]:
        if user["username"] == username:
            if user["balance"] >= amount:
                user["balance"] -= amount
                save_data(data)
                return user["balance"]
            else:
                return "INSUFFICIENT_FUNDS"

    return None


def transfer_money(sender_username, receiver_username, amount):
    data = load_data()

    sender = None
    receiver = None

    for user in data["users"]:
        if user["username"] == sender_username:
            sender = user
        if user["username"] == receiver_username:
            receiver = user

    if sender is None:
        return "SENDER_NOT_FOUND"

    if receiver is None:
        return "RECEIVER_NOT_FOUND"

    if sender["balance"] < amount:
        return "INSUFFICIENT_FUNDS"

    sender["balance"] -= amount
    receiver["balance"] += amount
    save_data(data)

    return sender["balance"]