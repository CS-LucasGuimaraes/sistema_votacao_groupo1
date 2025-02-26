from utils import http_parser_request
from utils import readjson
from utils import writejson

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

def http_get(socket_client, request):
    msgHeader = '' ; msgBody = ''

    if ('Connection' in request and request['Connection'] == 'keep-alive'):
        msgHeader = 'HTTP/1.1 200 OK \r\n' \
                    'Date: Tue, 09 Aug 2022 13:23:35 GMT\r\n' \
                    'Server: MyServer/0.0.1\r\n' \
                    'Content-Type: text/html\r\n' \
                    'Connection: keep-alive' \
                    '\r\n'
    else:
        msgHeader = 'HTTP/1.1 200 OK \r\n' \
                    'Date: Tue, 09 Aug 2022 13:23:35 GMT\r\n' \
                    'Server: MyServer/0.0.1\r\n' \
                    'Content-Type: text/html\r\n' \
                    '\r\n'

    candidates = ["1", '2'];

    if (request['Path'] == '/'):
        msgBody =   '<html>' \
                    '<head><title>Hello, World</title></head>' \
                    '<body><h1> Your first web server!</h1>' \
                    '<h3>Congratulation!!</h3>' \
                    '</body>' \
                    '</html>'
    if (request['Path'] == '/candidates'):
        msgBody =   '<html>' \
                    '<head><title>Candidates</title></head>' \
                    '<body>' \
                   f'<h3>{candidates[0]}</h3>' \
                   f'<h3>{candidates[1]}</h3>' \
                    '</body>'\
                    '</html>'

    msgHtml = msgHeader + msgBody

    socket_client.send(msgHtml.encode())

def http_post(socket_client, request):
    if request['path'] == '/sendkey':
        msgHeader = ''
        votou = False
        #adicionar o voto
        for client in readjson("keys"):
            if client['key'] == request['body']['key']: #caso a pessoa já votou
                votou = True
                #reply de já votou http_post()
                msgHeader = 'HTTP/1.1 500 Error \r\n' \
                            'Host: voting.com\r\n' \
                            'Content-Type: text/html\r\n' \
                            '\r\n'

        if votou == False:
            #adiciona a chave no keys.json
            keys_dados = readjson("keys")
            keys_dados.append({"key": request['body']['key']})
            writejson("keys", keys_dados)

            msgHeader = 'HTTP/1.1 200 OK \r\n' \
                        'Host: voting.com\r\n' \
                        'Content-Type: text/html\r\n' \
                        '\r\n'
            #reply o voto registrado
    if request['path'] == '/voting':
        ...
   
    socket_client.send(msgHeader.encode())

def handle_request(socket_client):
    
    keep_alive = True
    while keep_alive:
        keep_alive = False
        req = socket_client.recv(2048).decode()
        if(req == ''):
            socket_client.close()
            return
        
        request = http_parser_request(req)

        if ('Connection' in request and request['Connection'] == 'keep-alive'):
            keep_alive = True

        if(request['Method'] == 'GET'):
            http_get(socket_client, request)
    
        elif(request['Method'] == 'POST'):
            http_post(socket_client, request)
    
    return

def main():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(("localhost", 1010))
    print("Main Server initialized.")
    server_socket.listen()

    while 1:
        socket_client, addr_client = server_socket.accept()
        print(f"Established connection with {addr_client}")
        Thread(target=handle_request, args=(socket_client,)).start()

if __name__ == '__main__':
    main()        
