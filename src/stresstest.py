from client import client
from threading import Thread
from main import main
from time import sleep
from utils import readjson

def stress():
    main()

    for i in range(15):
        Thread(target=client, args=("stress", str(i), i%2)).start()
        # print(f"Client {i} started\n")
        # client("stress", str(i), i%2)
        # print(f"\nClient {i} finished\n")
        sleep(0.2)

  
    sleep(5)

    assert(readjson("election") ==  {
        "Candidato 1": 7,
        "Candidato 2": 8
    })

    assert(len(readjson("public_keys")) == 15)
    assert(len(readjson("private_keys"))== 15)

    print("\nTeste de estresse passou com sucesso.")

if __name__ == '__main__':
    stress()