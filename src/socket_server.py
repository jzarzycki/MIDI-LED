#!/usr/bin/env python3

import socket
import json

class Server():
    __HOST__ = '127.0.1.1'
    __PORT__ = 65432            # can use ports starting from 1024
    __data__ = {}
    __led__ = {}
    __server_on__ = False

    def __init__(self, led, data):
        self.__led__ = led
        self.__data__ = data
        self.__server_on__ = True

    def __del__(self):
        self.__server_on__ = False

    def convertColor(self, color):
        result = []
        for i in range(3):
            result.append(int("0x"+color[2*i+1:2*i+3], 0))
        return tuple(result)

    def __handle_data__(self, data):
        for trigger, animation in data.items():
            if animation is None:
                # no more animations left, delete whole trigger
                del self.__data__[trigger]
            else:
                for name, args in animation.items():
                    if type(args) == list:
                        # color cycling animation
                        colors = []
                        for color in args:
                            colors.append(self.convertColor(color))
                        if name == 'color-from-middle':
                            self.__led__.color_cycle_anim = colors
                            self.__led__.current_index_anim = 0
                            self.__led__.default_color_anim = self.__led__.__dim_color__(colors[0])
                            self.__led__.current_index = 0
                        else:
                            self.__led__.color_cycle = colors
                            self.__led__.current_index = 0
                            self.__led__.default_color = self.__led__.__dim_color__(colors[0])
                            self.__led__.current_index_anim = 0
                        if not trigger in self.__data__.keys():
                            self.__data__[trigger] = {}
                        self.__data__[trigger][name] = ()
                    else:
                        if args is None:
                            # delete this animation
                            del self.__data__[trigger][name]
                        else:
                            # brightness animation, argument is an int
                            if not trigger in self.__data__.keys():
                                self.__data__[trigger] = {}
                            self.__data__[trigger][name] = (int(args),)

    def run_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.__HOST__, self.__PORT__))
            s.listen()
            while self.__server_on__:
                data = None
                conn, addr = s.accept()
                with conn:
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        conn.sendall(b'ok')
                        obj = json.loads(data)
                        self.__handle_data__(obj)