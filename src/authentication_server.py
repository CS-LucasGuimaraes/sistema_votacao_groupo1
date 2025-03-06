from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from utils import readjson, writejson

def handle_request(socket_client):
    login = socket_client.recv(2048).decode()
    socket_client.send("ok".encode())

    public_key = socket_client.recv(2048).decode()
    socket_client.send("ok".encode())
    
    socket_client.close()
    
    keys = readjson("public_keys") or dict()
    keys[login] = [public_key, False]
    writejson(keys, "public_keys")


def auth_server():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(("localhost", 1020))
    print("Authentication Server initialized.")
    server_socket.listen()

    while 1:
        socket_client, addr_client = server_socket.accept()
        print(f"Established connection with {addr_client}")
        Thread(target=handle_request, args=(socket_client,)).start()

if __name__ == '__main__':
    auth_server()