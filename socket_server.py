#!/usr/bin/env python3

import socket
import json

__HOST__ = '127.0.1.1'
__PORT__ = 65432            # can use ports starting from 1024
__data__ = {}

def init(data):
    __data__ = data

def convertColor(color):
    result = []
    for i in range(3):
        result.append(int("0x"+color[2*i+1:2*i+3], 0))
    return tuple(result)

def __handle_data__(data):
    print(data)
    for trigger, animation in data.items():
        if animation != None:
            for name, args in animation.items():
                if type(args) == list:
                    print(convertColor(args[0]))

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((__HOST__, __PORT__))
        s.listen()
        while True:
            data = None
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(b'ok')
                    obj = json.loads(data)
                    __handle_data__(obj)

drums = {
    "snare": {
        "flash": 40
    },
    "kick": {
        "flash": 60
    },
    "hi-hat closed": {
        "flash": 12
    },
    "crash": {
        "flash": 70,
    },
    "ride": {
        "flash": 6,
    },
}

if __name__ == '__main__':
    run_server()