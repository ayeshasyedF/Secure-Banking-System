import socket

HOST = "127.0.0.1"
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

client_socket.send("Hello from client".encode())

reply = client_socket.recv(1024).decode()
print("Server replied:", reply)

client_socket.close()