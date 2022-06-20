#!/usr/bin/env python
# -*- coding: utf-8 -*-
from commonFuncs import *
import socket

def getAddress(): #получение адреса сервера
    host = input('Write hostname:')
    socket_number = input('Write socket:')
    if not host:
        host = 'localhost'
    if not socket_number or not socket_number.isdigit():
        socket_number = 1025
    else:
        socket_number = int(socket_number)
    return host, socket_number


def login(sock): #авторизация на сервере
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
    print(f'Connecting to server on port {host}, {socket_number}') #соединение с сервером
    sock.connect((host, socket_number))
    print('Connection established')
    if login(sock):
        while True:
            try:
                request = input('ftp>')
            except:
                break
            if request == '':
                continue
            sendP(sock, request) #отправление запросов
            response = getP(sock) #принятие ответов
            if response == 'exit':
                break
            print(response)
    print('End connection with server')

except KeyboardInterrupt as k:
    print(k)
except ConnectionRefusedError:
    print("Connection refused")
except Exception as s:
    print("Connection failed")
finally:
    sock.close()
