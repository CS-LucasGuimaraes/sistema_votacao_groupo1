from dns import dns
from authentication_server import auth_server
from main_server import server
from threading import Thread

from utils import writejson

def main():
    candidates = {
        "Candidato 1": 0,
        "Candidato 2": 0
    }
    
    writejson(candidates, "election")
    writejson({}, "public_keys")
    writejson({}, "private_keys")

    Thread(target=dns).start()
    Thread(target=auth_server).start()
    Thread(target=server, args=(1010,)).start()
    Thread(target=server, args=(1011,)).start()

if __name__ == '__main__':
    main()