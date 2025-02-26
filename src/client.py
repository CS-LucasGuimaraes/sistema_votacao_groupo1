from env import DNS_ADDRESS, DNS_PORT
from utils import http_parser_reply

from socket import socket, AF_INET, SOCK_STREAM

SERVER_ADDRESS = str()
SERVER_PORT = int()

def send_get_request(client_socket):
    msg = "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
    client_socket.send(msg.encode())

def get_addr():
    global SERVER_ADDRESS, SERVER_PORT

    try:
        addr = get_addr_from_name("voting.com").split(':')
        
        SERVER_ADDRESS = addr[0]
        SERVER_PORT = int(addr[1])
    except:
        print(Exception)
        raise("Erro ao conectar com o servidor DNS")
        

def connect_to_server(client_socket):
    try:
        client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
        return True
    except:
        print(Exception)
        try:
            get_addr()
        except:
            return
        
        try:
            client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
        except:
            raise("Erro ao conectar com o servidor")
        

def get_candidate_list(client_socket):
    try:
        try:
            connect_to_server(client_socket)
        except:
            exit()
    
        msg =  'GET /candidates HTTP/1.1\r\n' \
        f'Host: {SERVER_ADDRESS}:{SERVER_PORT}\r\n'
            # 'Content-Length: 31\r\n' \
            # '\r\n'
            # '{\r\n' \
            # 'vote": "candidato 1"\r\n ' \
            # '}'
        
        client_socket.send(msg.encode())
        
        recv = client_socket.recv(1024).decode()
        
        client_socket.close()
        
        return recv
    except:
        return None


def get_addr_from_name(name):
    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((DNS_ADDRESS, DNS_PORT))
        client_socket.send(name.encode())
        addr = client_socket.recv(1024).decode()
        client_socket.close()
        print("Endereço recebido do DNS: ", addr)
        return addr
    except:
        print("Erro ao conectar com o servidor DNS")
        return None

def main():    
    client_socket = socket(AF_INET, SOCK_STREAM)

    print(get_candidate_list(client_socket))
    print(get_candidate_list(client_socket))
    print(get_candidate_list(client_socket))
    print(get_candidate_list(client_socket))
    print(get_candidate_list(client_socket))

    while(1):
        pass

    # print(http_parser_reply(client_socket.recv(1024).decode()))

    # while (1):
    #     try:
    #         msg = input()
    #     except EOFError:
    #         break

    #     client_socket = socket(AF_INET, SOCK_STREAM)
    #     client_socket.connect(("127.0.0.1", 12345))

    #     client_socket.send(msg.encode())
    #     msg = http_parser(client_socket.recv(1024).decode())
    #     print(f"Mensagem recebida {msg}")

main()