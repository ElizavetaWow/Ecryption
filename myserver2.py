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
                    data = getP(self.conn)
                    if not data or (data == 'exit'):
                        sendP(self.conn, '')
                    else:
                        with lock2:
                            with open('history.txt', 'a') as history:
                                history.write(f'[{self.name}]: {data}\n')
                        sendAll(users, self, data.upper())
        except KeyboardInterrupt as k:
            with lock2:
                with open('log.txt', 'a') as log:
                    log.write(k)
        except ConnectionAbortedError:
            with lock2:
                with open('log.txt', 'a') as log:
                    log.write("Lost connection from client\n")
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
                    self.name = name
                else:
                    sendP(self.conn, "Login failed. Goodbye!")
                    result = False
            else:
                if not nameEnter or not passwordEnter:
                    sendP(self.conn, "Wrong input values!")
                    result = False
                else:
                    client_dict[key] = [nameEnter, passwordEnter]
                    self.name = nameEnter
                    sendP(self.conn, "Registration completed")
            with open('clients.json', 'w') as cl:
                json.dump(client_dict, cl)
        return result


class PortsListen(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self, name=str(sock))
        self.sock = sock

    def run(self):
        global is_running
        try:
            while is_running:
                self.sock.settimeout(1)
                try:
                    conn, addr = self.sock.accept()
                    users.append(User(conn, addr))
                    with open('log.txt', 'a') as log:
                        log.write('Connection established:' + str(addr) + '\n')
                    users[-1].start()
                    for u in users:
                        if not u.is_alive():
                            users.remove(u)
                except socket.timeout:
                    continue
        except KeyboardInterrupt as k:
            with open('log.txt', 'a') as log:
                log.write(k)
        except ConnectionResetError:
            with open('log.txt', 'a') as log:
                log.write("Lost connection from client\n")
        except FinalError as e:
            with open('log.txt', 'a') as log:
                log.write(e.txt + "\n")


class FinalError(Exception):
    def __init__(self, text):
        self.txt = text


lock = threading.Lock()
lock2 = threading.Lock()
is_running = True
commandList = ["exit", "pause", "show logs", "clean logs", "clean logins"]
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
sock.listen(0)
with open('log.txt', 'a') as log:
    log.write('Server\'s socket is ' + str(sock.getsockname()[1]) + '\n')
try:
    pl = PortsListen(sock)
    pl.start()
    for i, e in enumerate(commandList):
        print(i + 1, " ", e)
    while True:
        command = input("Print command number: ")
        if command == "1":
            is_running = False
            break
        if command == "2":
            is_running = False
            print("Done")
        if command == "3":
            log = open('log.txt', 'r')
            print("Logs: [")
            for i in log.readlines():
                print(i, end='')
            print("]")
            log.close()
            print("Done")
        if command == "4":
            log = open('log.txt', 'w')
            log.close()
            print("Done")
        if command == "5":
            with open('clients.json', 'w') as cl:
                client_dict = dict()
                json.dump(client_dict, cl)
            print("Done")
except KeyboardInterrupt as k:
    with open('log.txt', 'a') as log:
        log.write(k)
except ConnectionResetError:
    with open('log.txt', 'a') as log:
        log.write("Lost connection from client\n")
except FinalError as e:
    with open('log.txt', 'a') as log:
        log.write(e.txt + "\n")
with open('log.txt', 'a') as log:
    log.write('Server stops working\n')
pl.join()
sock.close()
