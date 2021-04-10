#!/usr/bin/env python
# -*- coding: utf-8 -*-
from commonFuncs import *
import socket
import threading

class Sender(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self, name=str(sock))
        self.sock = sock

    def run(self):
        try:
            while True:
                msg = input()
                if not msg or msg == 'exit':
                    sendP(self.sock, msg)
                    return
                sendP(self.sock, msg)
        except KeyboardInterrupt as k:
            sendP(self.sock, '')
            print(k)
        except ConnectionRefusedError:
            print("Connection refused")
        except Exception as s:
            print(s)

class Listener(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self, name=str(sock))
        self.sock = sock

    def run(self):
        while True:
            data = getP(sock)
            if not data:
                return
            print(data)

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
status = True
try:
    host, socket_number = getAddress()
    print(f'Connecting to server on port {host}, {socket_number}')
    sock.connect((host, socket_number))
    print('Connection established')
    if login(sock):
        listener = Listener(sock)
        listener.start()
        sender = Sender(sock)
        sender.start()
        sender.join()
        listener.join()
    print('End connection with server')

except KeyboardInterrupt as k:
    print(k)
except ConnectionRefusedError:
    print("Connection refused")
except Exception as s:
    print("Connection failed")
finally:
    sock.close()
