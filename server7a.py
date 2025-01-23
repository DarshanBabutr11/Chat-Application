import socket
import ssl
import threading

def handle_client(client_socket, client_address):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"[{client_address[0]}:{client_address[1]}] says: {message}")
            broadcast(f"[{client_address[0]}:{client_address[1]}] says: {message}", client_socket)
        except:
            break

    client_socket.close()
    print(f"Connection closed: {client_address[0]}:{client_address[1]}")

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                clients.remove(client)

def send_message(message, client_socket):
    try:
        client_socket.send(message.encode())
    except:
        clients.remove(client_socket)

clients = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 8080))
server_socket.listen()

# Load SSL/TLS certificate and key
certfile = "server.crt"
keyfile = "server.key"
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile, keyfile)

# Wrap the socket with SSL/TLS
ssl_socket = ssl_context.wrap_socket(server_socket, server_side=True)

print("Server started. Listening for connections...")

while True:
    client_socket, client_address = ssl_socket.accept()
    print(f"New connection: {client_address[0]}:{client_address[1]}")
    clients.append(client_socket)
    threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

    # Send welcome message to new client
    send_message("Welcome to the chat room!", client_socket)

    # Send notification to other clients
    broadcast(f"A new user has joined the chat: {client_address[0]}:{client_address[1]}", client_socket)

    # Send a message from the server to the new client
    send_message("This is a message from the server", client_socket)