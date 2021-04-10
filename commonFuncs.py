#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket


def sendP(sock, data):
    prefix = str(len(data)).zfill(10)
    sock.send((prefix + data).encode())

def sendAll(users, client, data):
    for user in users:
        if user.is_alive() and user.conn != client.conn:
            sendP(user.conn, '['+client.name+']: '+data)


def getP(sock):
    try:
        prefix = sock.recv(10)
        msg_length = int(prefix.decode())
        data = sock.recv(msg_length)
        return data.decode()
    except Exception:
        return None

def createSock(host='localhost'):
    sock = socket.socket()
    for i in range(1, 2 ** 16 - 1):
        try:
            sock.bind((host, i))
            print(f"Server host -> {host} \nPort -> {i}")
            return sock
        except socket.error:
            pass