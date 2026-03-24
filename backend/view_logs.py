from backend.audit import read_decrypted_logs


def main():
    logs = read_decrypted_logs()

    print("\nDecrypted Audit Logs:\n")

    if not logs:
        print("No logs found.")
        return

    for entry in logs:
        print(entry)


if __name__ == "__main__":
    main()