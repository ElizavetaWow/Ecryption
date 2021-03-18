#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket, sys

def getData(conn, n):
    try:
        data = conn.recv(n)
        return data, True
    except ConnectionResetError as e:
        print(e)
        print("Lost connection from server\n")
    except Exception as s:
        print(s)
    return "Exception", False


def getInput(msg):
    try:
        promt = input(msg)
        return promt, True 
    except KeyboardInterrupt as k:
        print(k)
        return "Exception", False

    
sock = socket.socket()
host = getInput('Write hostname:')
if not(host[1]):
    print("Stop program")
    exit()
socnum = getInput('Write socket:')
if  not(socnum[1]):
    print("Stop program")
    exit()
host, socnum = host[0], socnum[0] 
if not host:
    host = 'localhost'
if not socnum:
    socnum = 1025
print('Connecting to server')
try:
    sock.connect((host, int(socnum)))
except ConnectionRefusedError as c:
    print("Connection refused")
    exit()
except ValueError as v:
    print("Invalid socket data. Connection refused")
    exit()

print('Connection established')

data, status  = getData(sock, 1024)
if not status:
    sock.close()
    exit()
if 'what is your name?' in data.decode():
    name, sts = getInput("Hello, what's your name?\n")
    if not sts:
        exit()
    sock.send(name.encode())
else:
    print(data.decode())

s = "start"
while s != "exit":
    s, sts = getInput('Write message to server\n')
    if not sts or not s:
        break
    sock.send(s.encode())
    print('Receiving data from server')
    data, status  = getData(sock, 1024)
    if not status:
        sock.close()
        print('End connection with server')
        exit()
    print('Answer: ', data.decode())
sock.send('exit'.encode())


print('End connection with server')
sock.close()
