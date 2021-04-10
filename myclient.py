#!/usr/bin/env python
# -*- coding: utf-8 -*-
from commonFuncs import *
import socket


def getAddress():
    host = input('Write hostname:')
    socket_number = input('Write socket:')
    if not host:
        host = 'localhost'
    if not socket_number or not socket_number.isdigit():
        socket_number = 1025
    else:
        socket_number = int(socket_number)
    return host, socket_number


def login(sock):
    data = getP(sock)
    sendP(sock, input(data))
    data = getP(sock)
    sendP(sock, input(data))
    data = getP(sock)
    print(data)
    if "completed" in data:
        return True
    else:
        return False


sock = socket.socket()
sock.setblocking(1)

try:
    host, socket_number = getAddress()
    print(f'Connecting to server on port {host}, {socket_number}')
    sock.connect((host, socket_number))
    print('Connection established')
    if login(sock):
        while True:
            msg = input('Write message to server\n')
            if not msg:
                break
            sendP(sock, msg)
            data = getP(sock)
            if not data:
                break
            print(data)
    print('End connection with server')

except KeyboardInterrupt as k:
    print(k)
except ConnectionRefusedError:
    print("Connection refused")
except Exception as s:
    print(s)
finally:
    sock.close()
