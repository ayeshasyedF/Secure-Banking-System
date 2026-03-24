import socket

HOST = "127.0.0.1"
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Server listening on {HOST}:{PORT}")

client_socket, client_address = server_socket.accept()
print(f"Connected by {client_address}")

message = client_socket.recv(1024).decode()
print("Client says:", message)

client_socket.send("Hello from server".encode())

client_socket.close()
server_socket.close()