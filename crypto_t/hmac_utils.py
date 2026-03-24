import hmac
import hashlib


def generate_hmac(message, key):
    return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()


def verify_hmac(message, key, received_hmac):
    calculated_hmac = generate_hmac(message, key)
    return hmac.compare_digest(calculated_hmac, received_hmac)