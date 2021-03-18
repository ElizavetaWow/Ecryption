#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket, errno
import json

def getData(conn, n):
    try:
        data = conn.recv(n)
        return data, True
    except ConnectionResetError as e:
        log.write("Lost connection from client\n")
    except KeyboardInterrupt as k:
        log.write("Stop program\n")
        log.write("Lost connection from client\n")
    return "Exception", False


try:
    open('clients.json', 'r')
except FileNotFoundError as e:
    with open('clients.json', 'w') as cl:
        cldict = dict()
        json.dump(cldict, cl) 

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
    log.write('Server\'s socket is '+str(sock.getsockname()[1])+'\n')
    while True:
        log.write('Server lisening the socket\n')
        sock.listen(1)
        try:
            conn, addr = sock.accept()
        except KeyboardInterrupt as k:
            log.write("Stop program")
            exit()

        log.write('Connection established:'+ str(addr)+ '\n')
        with open('clients.json', 'r') as cl:
            cldict = json.load(cl)
            if cldict.get(str(addr[1])) != '' and cldict.get(str(addr[1])) != None:
                hello = "Hello, "+str(cldict.get(str(addr[1])))
                conn.send(hello.encode())
            else:
                conn.send("Hello, what is your name?".encode())
                name, status = getData(conn, 1024)
                if not status:
                    conn.close()
                    continue
                cldict[str(addr[1])]=name.decode()
        log.write('Server write to json file\n')
        with open('clients.json', 'w') as cl:
            json.dump(cldict, cl)
        log.write('Server receiving data from client\n')
        while True:
            data, status = getData(conn, 1024)
            if not status:
                break
            if data == 'exit'.encode():
                break
            if data:
                log.write('Server sending data to client\n')
                conn.send(data.upper())

        log.write('Server stops connection with'+  str(addr)+ '\n')    
        conn.close()

    log.write('Server stops working\n')
