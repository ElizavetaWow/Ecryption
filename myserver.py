#!/usr/bin/env python
# -*- coding: utf-8 -*-

import errno, socket
import json
import SocketPlus

def sendP(conn, data):
    prefix = str(len(data)).zfill(10)
    conn.send((prefix + data).encode())

def getP(conn):
    try:
        prefix = conn.recv(10)
        msg_length = int(prefix.decode())
        data = conn.recv(msg_length)
        return data.decode()
    except Exception:
        return None

try:
    open('clients.json', 'r')
except FileNotFoundError as e:
    with open('clients.json', 'w') as cl:
        client_dict = dict()
        json.dump(client_dict, cl)

with open('log.txt', 'a') as log:
    log.write('Server starts working\n')
    sock = SocketPlus.SocketPlus()
    try:
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
            conn, addr = sock.accept()
            log.write('Connection established:' + str(addr) + '\n')
            with open('clients.json', 'r') as cl:
                client_dict = json.load(cl)
                if client_dict.get(str(addr[1])) != '' and client_dict.get(str(addr[1])) is not None:
                    hello = "Hello, " + str(client_dict.get(str(addr[1])))
                    sendP(conn, hello)
                else:
                    sendP(conn, "Hello, what is your name?")
                    name = getP(conn)
                    if not name:
                        conn.close()
                        continue
                    client_dict[str(addr[1])] = name
            log.write('Server write to json file\n')
            with open('clients.json', 'w') as cl:
                json.dump(client_dict, cl)
            log.write('Server receiving data from client\n')
            while True:
                data = getP(conn)
                if not data or (data == 'exit'):
                    sendP(conn, '')
                    break
                log.write('Server sending data to client\n')
                sendP(conn, data.upper())

            log.write('Server stops connection with' + str(addr) + '\n')
            conn.close()
    except KeyboardInterrupt as k:
        log.write(k)
    except ConnectionResetError:
        log.write("Lost connection from client\n")
    log.write('Server stops working\n')
    sock.close()
