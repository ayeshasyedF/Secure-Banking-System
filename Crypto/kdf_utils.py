import hashlib


def derive_keys(master_secret):
    encryption_key = hashlib.sha256((master_secret + "_enc").encode()).hexdigest()
    mac_key = hashlib.sha256((master_secret + "_mac").encode()).hexdigest()

    return encryption_key, mac_key