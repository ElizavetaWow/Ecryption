#!/usr/bin/env python
# -*- coding: utf-8 -*-

from user import *
import socket
import threading
from commonFuncs import *

def createSock(host='localhost'):
    sock = socket.socket()
    for i in range(1, 2 ** 16 - 1):
        try:
            sock.bind((host, i))
            print(f"Address: {host} [{i}]")
            return sock
        except socket.error:
            pass

try:
    open('clients.json', 'r')
except FileNotFoundError as e:
    with open('clients.json', 'w') as cl:
        client_dict = dict()
        json.dump(client_dict, cl)
users = list()
with open('log.txt', 'a') as log:
    log.write('Server starts working\n')
try:
    sock = createSock()
    with open('log.txt', 'a') as log:
        log.write('Server\'s socket is ' + str(sock.getsockname()[1]) + '\n')
    while True:
        sock.listen(0)
        conn, addr = sock.accept()
        users.append(User(conn, addr))
        with open('log.txt', 'a') as log:
            log.write('Connection established:' + str(addr) + '\n')
        users[-1].start()
        print(users)
        for u in users:
            if not u.is_alive():
                users.remove(u)
except KeyboardInterrupt as k:
    with open('log.txt', 'a') as log:
        log.write(k)
except ConnectionResetError:
    with open('log.txt', 'a') as log:
        log.write("Lost connection from client\n")
with open('log.txt', 'a') as log:
    log.write('Server stops working\n')
sock.close()
