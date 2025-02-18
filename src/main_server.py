from utils import http_parser_request

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

def http_get(socket_client):
    msgHeader = 'HTTP/1.1 200 OK \r\n' \
                'Date: Tue, 09 Aug 2022 13:23:35 GMT\r\n' \
                'Server: MyServer/0.0.1\r\n' \
                'Content-Type: text/html\r\n' \
                '\r\n'
    msgBody = '<html>' \
              '<head><title>Hello, World</title></head>' \
              '<body><h1> Your first web server!</h1>' \
              '<h3>Congratulation!!</h3>' \
              '</body>' \
              '</html>'

    msgHtml = msgHeader + msgBody

    socket_client.send(msgHtml.encode())

def http_post():
    ...

def handle_request(socket_client):
    req = socket_client.recv(2048).decode()
    if(req == ''):
        socket_client.close()
        return
    
    request = http_parser_request(req)

    if(request['Method'] == 'GET'):
        http_get(socket_client)
    
    elif(request['Method'] == 'POST'):
        http_post()
    
    return

def main():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(("localhost", 1011))

    print("Server Socket initialized.")
    server_socket.listen()

    while 1:
        socket_client, addr_client = server_socket.accept()
        print(f"Established connection with {addr_client}")
        Thread(target=handle_request, args=(socket_client,)).start()

if __name__ == '__main__':
    main()        
