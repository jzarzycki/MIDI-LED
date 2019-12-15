#!/usr/bin/env python3

import socket
import json

__HOST__ = '127.0.1.1'
__PORT__ = 65432            # can use ports starting from 1024
__data__ = {}
__led__ = {}
__server_on__ = False

def init(led, data):
    global __led__
    __led__ = led
    global __data__
    __data__ = data
    global __server_on__
    __server_on__ = True

def shutdown():
    global __server_on__
    __server_on__ = False

def convertColor(color):
    result = []
    for i in range(3):
        result.append(int("0x"+color[2*i+1:2*i+3], 0))
    return tuple(result)

def __handle_data__(data):
    for trigger, animation in data.items():
        if animation is None:
            # no more animations left, delete whole trigger
            del __data__[trigger]
        else:
            for name, args in animation.items():
                if type(args) == list:
                    # color cycling animation
                    colors = []
                    for color in args:
                        colors.append(convertColor(color))
                    if name == 'color-from-middle':
                        __led__.color_cycle_anim = colors
                        __led__.current_index_anim = 0
                        __led__.default_color_anim = __led__.__dim_color__(colors[0])
                        __led__.current_index = 0
                    else:
                        __led__.color_cycle = colors
                        __led__.current_index = 0
                        __led__.default_color = __led__.__dim_color__(colors[0])
                        __led__.current_index_anim = 0
                    if not trigger in __data__.keys():
                        __data__[trigger] = {}
                    __data__[trigger][name] = ()
                else:
                    if args is None:
                        # delete this animation
                        del __data__[trigger][name]
                    else:
                        # brightness animation, argument is an int
                        if not trigger in __data__.keys():
                            __data__[trigger] = {}
                        arg = convertColor(args)
                        __data__[trigger][name] = (arg,)

def run_server():
    global __server_on__
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((__HOST__, __PORT__))
        s.listen()
        while __server_on__:
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