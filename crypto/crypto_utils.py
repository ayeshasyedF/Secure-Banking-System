import json
import struct

from crypto.aes_utils import encrypt_message, decrypt_message
from crypto.hmac_utils import generate_hmac, verify_hmac

DEBUG_MODE = True


def send_packet(sock, data):
    encoded_data = data.encode("utf-8")
    packet_length = struct.pack("!I", len(encoded_data))
    sock.sendall(packet_length + encoded_data)


def receive_exact_bytes(sock, num_bytes):
    data = b""

    while len(data) < num_bytes:
        chunk = sock.recv(num_bytes - len(data))

        if not chunk:
            return None

        data += chunk

    return data


def receive_packet(sock):
    header = receive_exact_bytes(sock, 4)

    if header is None:
        return None

    message_length = struct.unpack("!I", header)[0]
    payload = receive_exact_bytes(sock, message_length)

    if payload is None:
        return None

    return payload.decode("utf-8")


def secure_send(sock, plaintext_message, encryption_key, mac_key):
    ciphertext = encrypt_message(plaintext_message, encryption_key)
    message_hmac = generate_hmac(ciphertext, mac_key)

    packet = {
        "ciphertext": ciphertext,
        "hmac": message_hmac
    }

    send_packet(sock, json.dumps(packet))


def secure_receive(sock, encryption_key, mac_key, receiver_name="RECEIVER"):
    packet_text = receive_packet(sock)

    if packet_text is None:
        return None, "NO_DATA"

    try:
        packet = json.loads(packet_text)
    except json.JSONDecodeError:
        return None, "INVALID_PACKET"

    if "ciphertext" not in packet or "hmac" not in packet:
        return None, "INVALID_PACKET"

    ciphertext = packet["ciphertext"]
    received_hmac = packet["hmac"]

    if DEBUG_MODE:
        print(f"\n--- {receiver_name} RECEIVED MESSAGE ---")
        print("Ciphertext:", ciphertext)
        print("HMAC:", received_hmac)

    if not verify_hmac(ciphertext, mac_key, received_hmac):
        if DEBUG_MODE:
            print("HMAC Verification: FAILED")
            print("------------------------------\n")
        return None, "HMAC_FAILED"

    if DEBUG_MODE:
        print("HMAC Verification: PASSED")

    try:
        plaintext = decrypt_message(ciphertext, encryption_key)
    except Exception:
        return None, "DECRYPTION_FAILED"

    if DEBUG_MODE:
        print("Decrypted Message:", plaintext)
        print("------------------------------\n")

    return plaintext, None