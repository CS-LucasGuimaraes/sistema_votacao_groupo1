from env import DNS_ADDRESS, DNS_PORT
from utils import readjson, writejson
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from time import sleep

from threading import Lock

private_keys_mutex = Lock()

from socket import socket, AF_INET, SOCK_STREAM

def get_addr(name):
    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((DNS_ADDRESS, DNS_PORT))

        client_socket.send(name.encode())
        addr = client_socket.recv(1024).decode()
        client_socket.close()
        print("Endereço recebido do DNS: ", addr)
        return addr.split(':')
    except:
        print("Erro ao conectar com o servidor DNS")
        return None

def client(mode, login, vote):
    if mode == "interative":
        login = str(input("Digite seu login: "))

    keys = readjson("private_keys") or {}

    if login not in list(keys.keys()):
        client_socket = socket(AF_INET, SOCK_STREAM)
        

        private_key = RSA.generate(1024)
        public_key = private_key.publickey()

        with private_keys_mutex:
            keys = readjson("private_keys") or {}
            keys[login] = private_key.export_key().decode()
            writejson(keys, "private_keys")

        auth_ip = get_addr("auth.com")
        client_socket.connect((auth_ip[0], int(auth_ip[1])))

        client_socket.send(login.encode())
        ok = client_socket.recv(1024).decode()
        client_socket.send(public_key.export_key())
        ok = client_socket.recv(1024).decode()
        client_socket.close()
    else:
        private_key = RSA.import_key(keys[login])
    
    for i in range(2):
        try:
            voting_ip = get_addr("voting.com")
            client_socket = socket(AF_INET, SOCK_STREAM)
            client_socket.connect((voting_ip[0], int(voting_ip[1])))

            client_socket.send(f"{login}".encode()) # mando meu id
            ok = client_socket.recv(1024).decode()
            client_socket.send(f"get candidates".encode())
            candidates = client_socket.recv(1024).decode().split(',')
            for i in range(len(candidates)):
                candidates[i] = candidates[i].replace("[","").replace("]","").replace("'","").strip()
                if (mode == "interative"): print(f"[{i+1}] {candidates[i]}")

            client_socket.send("vote".encode())
            if (mode == "interative"): vote = int(input("Digite o número do candidato: "))
            
            candidate_name = candidates[vote-1].encode()
            hash_vote = SHA256.new(candidate_name)
            signature = pkcs1_15.new(private_key).sign(hash_vote)

            client_socket.send(signature)
            ok = client_socket.recv(1024).decode()
            client_socket.send(candidate_name) 
            print(client_socket.recv(1024).decode())
            client_socket.close()
            break
        except:
            print("Erro ao conectar com o servidor de votação")
            if (i == 0):
                if (mode == "interative"): print("Tentando novamente...")
            else:
                print("Erro ao conectar com o servidor de votação. Tente novamente mais tarde.")
                return

    if (mode == "interative"): 
        while 1:
            client_socket = socket(AF_INET, SOCK_STREAM)
            voting_ip = get_addr("voting.com")
            client_socket.connect((voting_ip[0], int(voting_ip[1])))
            client_socket.send(f"result".encode())
            print("\nResultado da votação:")
            print(client_socket.recv(1024).decode())
            client_socket.close()
            sleep(5)


if __name__ == '__main__':
    client("interative", "", "")