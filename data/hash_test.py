import hashlib

print(hashlib.sha256("1234".encode()).hexdigest())
print(hashlib.sha256("5678".encode()).hexdigest())
print(hashlib.sha256("8765".encode()).hexdigest())
print(hashlib.sha256("4321".encode()).hexdigest())
