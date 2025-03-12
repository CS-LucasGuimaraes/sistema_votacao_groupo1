import json
from threading import Lock

read_writemutex = Lock()

def readjson(path):
    with read_writemutex:
        f = open("./data/" + path + ".json", 'r')
        data = json.load(f)
        f.close()
        return data

def writejson(data, path):
    with read_writemutex:
        f = open("./data/" + path + ".json", 'w')
        json.dump(data, f)
        f.close()
