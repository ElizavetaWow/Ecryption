#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket


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
        prompt = input(msg)
        return prompt, True
    except KeyboardInterrupt as k:
        print(k)
        return "Exception", False


sock = socket.socket()
host = getInput('Write hostname:')
if not (host[1]):
    print("Stop program")
    exit()
socket_number = getInput('Write socket:')
if not (socket_number[1]):
    print("Stop program")
    exit()
host, socket_number = host[0], socket_number[0]
if not host:
    host = 'localhost'
if not socket_number:
    socket_number = 1025
print(f'Connecting to server on port {host}, {socket_number}')
try:
    sock.connect((host, int(socket_number)))
except ConnectionRefusedError:
    print("Connection refused")
    exit()
except ValueError:
    print("Invalid socket data. Connection refused")
    exit()

print('Connection established')

data, status = getData(sock, 1024)
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
    data, status = getData(sock, 1024)
    if not status:
        sock.close()
        print('End connection with server')
        exit()
    print(data.decode())
sock.send('exit'.encode())

print('End connection with server')
sock.close()
