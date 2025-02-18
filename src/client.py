from env import DNS_ADDRESS, DNS_PORT
from utils import http_parser_reply

from socket import socket, AF_INET, SOCK_STREAM

def send_get_request(client_socket):
    msg = "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
    client_socket.send(msg.encode())

def get_addr_from_name(name):
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((DNS_ADDRESS, DNS_PORT))
    client_socket.send(name.encode())
    addr = client_socket.recv(1024).decode()
    client_socket.close()
    return addr

def print_menu(idx):
    menu_text = {
    1:
        'Bem vindo ao sistema de votação!\n' \
        '[0] Fechar programa\n' \
        '[1] Conectar-se ao servidor\n'
    ,
    2:
        'Você tem certea que deseja sair? Você não poderá voltar a executar\n' \
        '[0] Não, voltar à tela anterior\n' \
        '[1] Sim, desejo encerrar a sessão\n'
    }

    print(menu_text[idx])


def menu():
    ...

def main():
    addr = get_addr_from_name("voting.com").split(':')
    
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((addr[0], int(addr[1])))
    
    i = 1
    while(i):
        send_get_request(client_socket)
        print("OK")
        # print(http_parser_reply(client_socket.recv(1024).decode()))
        i = input()

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