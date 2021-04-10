#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import threading
import json
from commonFuncs import *


class User(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self, name=str(addr[0]) + " " + str(addr[1]))
        self.host = addr[0]
        self.port = addr[1]
        self.conn = conn

    def run(self):
        try:
            if self.authentication():
                while True:
                    with lock2:
                        with open('log.txt', 'a') as log:
                            log.write('Server sending data to ' + str(self.host) + " " + str(self.port) + '\n')
                    data = getP(self.conn)
                    if not data or (data == 'exit'):
                        sendP(self.conn, '')
                        break
                    sendAll(users, self.conn, data.upper())
        except KeyboardInterrupt as k:
            with lock2:
                with open('log.txt', 'a') as log:
                    log.write(k)
        except ConnectionResetError:
            with lock2:
                with open('log.txt', 'a') as log:
                    log.write("Lost connection from client\n")
        with lock2:
            with open('log.txt', 'a') as log:
                log.write('Server stops connection with ' + str(self.host) + " " + str(self.port) + '\n')
        self.conn.close()

    def authentication(self):
        with lock:
            with open('clients.json', 'r') as cl:
                client_dict = json.load(cl)
            key = str(self.host) + " " + str(self.port)
            sendP(self.conn, "Enter your name: ")
            nameEnter = getP(self.conn)
            sendP(self.conn, "Enter the password: ")
            passwordEnter = getP(self.conn)
            result = True
            if key in client_dict.keys():
                name, password = client_dict.get(key)
                if name == nameEnter and password == passwordEnter:
                    sendP(self.conn, "Login completed")
                else:
                    sendP(self.conn, "Login failed. Goodbye!")
                    result = False
            else:
                if not nameEnter or not passwordEnter:
                    sendP(self.conn, "Wrong input values!")
                    result = False
                client_dict[key] = [nameEnter, passwordEnter]
                sendP(self.conn, "Registration completed")
            with open('clients.json', 'w') as cl:
                json.dump(client_dict, cl)
        return result


lock = threading.Lock()
lock2 = threading.Lock()
try:
    open('clients.json', 'r')
except FileNotFoundError as e:
    with open('clients.json', 'w') as cl:
        client_dict = dict()
        json.dump(client_dict, cl)
users = list()
with open('log.txt', 'a') as log:
    log.write('Server starts working\n')
sock = createSock()
try:
    with open('log.txt', 'a') as log:
        log.write('Server\'s socket is ' + str(sock.getsockname()[1]) + '\n')
    while True:
        sock.listen(0)
        conn, addr = sock.accept()
        users.append(User(conn, addr))
        with open('log.txt', 'a') as log:
            log.write('Connection established:' + str(addr) + '\n')
        users[-1].start()
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
