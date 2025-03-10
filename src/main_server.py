from utils import readjson
from utils import writejson

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15 
from Crypto.Hash import SHA256

vote_limit = {}
end = False

def handle_request(socket_client, port):
    global vote_limit, end
    login = ''
    while 1:
        if (end): 
            # mandar mensagem de encerramento
            socket_client.close()
            return

        req = socket_client.recv(2048).decode()
        
        if (req == ''):
            socket_client.close()
            return
    
        elif (req == 'get candidates'):
            candidates = list(readjson("election").keys())
            socket_client.send(str(candidates).encode())
        
        elif (req == "vote"):            
            signature = socket_client.recv(2048)
            socket_client.send("ok".encode())
            vote = socket_client.recv(2048).decode()

            hash_vote = SHA256.new(vote.encode())

            public_key = RSA.import_key(readjson("public_keys")[login][0])

            try:
                pkcs1_15.new(public_key).verify(hash_vote, signature)
                print("Assinatura válida")

                if (login in readjson("public_keys") and readjson("public_keys")[login][1] == False):
                    candidates = readjson("election")
                    candidates[vote] += 1
                    vote_limit[port] += 1

                    writejson(candidates, "election")

                    keys = readjson("public_keys")
                    keys[login][1] = True
                    writejson(keys, "public_keys")
                    print("Voto computado com sucesso")
                    socket_client.send("Voto computado com sucesso!".encode())
                else:
                    print("Voto inválido")
                    socket_client.send("Voto inválido! Usuário não cadastrado ou usuário já votou.".encode())

            except:
                print("Assinatura inválida")
                socket_client.send("Voto inválido! Assinatura inválida.".encode())

            

        elif (req == "result"):
            candidates = readjson("election")
            socket_client.send(str(candidates).encode())
            socket_client.close()
            return
        
        else: # req == login
            login = req
            socket_client.send("ok".encode())

    return

def server(port):
    global end, vote_limit

    vote_limit[port] = 0
    
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(("localhost", int(port)))
    print("Main Server initialized.")
    server_socket.listen()

    while 1:
        if vote_limit[port] == 8:
            print("Vote limit reached. Shutting down server...")
            break
        
        election = readjson("election") or dict()
        votes = 0
        for v in list(election.values()):
            votes += v

        if votes == 15:
            end = True
            print("Vote limit reached. Shutting down server...")
            break

        socket_client, addr_client = server_socket.accept()
        # print(f"Established connection with {addr_client}")
        Thread(target=handle_request, args=(socket_client, port)).start()    

if __name__ == '__main__':
    server(1010)