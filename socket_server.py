#!/usr/bin/env python3

import socket
import json

HOST = '192.168.1.14'
PORT = 65432            # Port to listen on (non-privileged ports are > 1023)

def handle_data(data):
    print(data)
    # print(drums)

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
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
                    handle_data(obj)
                    # if data == b'end_conn':
                    #     conn.sendall(b'Goodbye from Windows\n')
                    #     conn.close()
                    #     break

drums = {
    "snare": {
        "flash": 40
    },
    "kick": {
        "wave-mid": 60
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