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