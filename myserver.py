#!/usr/bin/env python
# -*- coding: utf-8 -*-

import errno
import json
import socket


def getData(conn, n):
    try:
        data = conn.recv(n)
        return data, True
    except ConnectionResetError:
        log.write("Lost connection from client\n")
    except KeyboardInterrupt:
        log.write("Stop program\n")
        log.write("Lost connection from client\n")
    return "Exception", False


try:
    open('clients.json', 'r')
except FileNotFoundError as e:
    with open('clients.json', 'w') as cl:
        client_dict = dict()
        json.dump(client_dict, cl)

with open('log.txt', 'a') as log:
    log.write('Server starts working\n')
    sock = socket.socket()
    for i in range(1025, 65536):
        try:
            sock.bind(('', i))
            break
        except socket.error as e:
            if e.errno != errno.EADDRINUSE:
                log.write(e)
    log.write('Server\'s socket is ' + str(sock.getsockname()[1]) + '\n')
    while True:
        log.write('Server listen the socket\n')
        sock.listen(1)
        try:
            conn, addr = sock.accept()
        except KeyboardInterrupt as k:
            log.write("Stop program")
            exit()

        log.write('Connection established:' + str(addr) + '\n')
        with open('clients.json', 'r') as cl:
            client_dict = json.load(cl)
            if client_dict.get(str(addr[1])) != '' and client_dict.get(str(addr[1])) is not None:
                hello = "Hello, " + str(client_dict.get(str(addr[1])))
                conn.send(hello.encode())
            else:
                conn.send("Hello, what is your name?".encode())
                name, status = getData(conn, 1024)
                if not status:
                    conn.close()
                    continue
                client_dict[str(addr[1])] = name.decode()
        log.write('Server write to json file\n')
        with open('clients.json', 'w') as cl:
            json.dump(client_dict, cl)
        log.write('Server receiving data from client\n')
        while True:
            data, status = getData(conn, 1024)
            if not status or (data == 'exit'.encode()):
                break
            if data:
                log.write('Server sending data to client\n')
                conn.send(data.upper())

        log.write('Server stops connection with' + str(addr) + '\n')
        conn.close()

    log.write('Server stops working\n')
