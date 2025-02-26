from env import DNS_ADDRESS, DNS_PORT
from utils import readjson

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

def handle_request(socket_client):
    request = socket_client.recv(2048).decode()

    dns_client = socket(AF_INET, SOCK_STREAM)

    for site in readjson('./data/dns.json'):
        if site['name'] == request:
            for addr in site['addr']: 
                try:
                    dns_client.connect((addr['ip'], addr['port']))
                    dns_client.close()
                    socket_client.send(f"{addr['ip']}:{addr['port']}".encode())
                    socket_client.close()
                except:
                    print(f"{addr['ip']}:{addr['port']} is down.")
                    continue
                    
    socket_client.close()
    return

def main():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((DNS_ADDRESS, DNS_PORT))

    print("DNS initialized.")
    server_socket.listen()

    while 1:
        socket_client, addr_client = server_socket.accept()
        print(f"Established connection with {addr_client}")
        Thread(target=handle_request, args=(socket_client,)).start()

main()        
