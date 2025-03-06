from client import client
from threading import Thread

def main():
    for i in range(15):
        Thread(target=client, args=("batch", str(i), i%2)).start()

if __name__ == '__main__':
    main()