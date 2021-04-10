#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket


def sendP(sock, data):
    prefix = str(len(data)).zfill(10)
    sock.send((prefix + data).encode())

def sendAll(socks, data):
    for sock in socks:
        sendP(sock, data)

def getP(sock):
    try:
        prefix = sock.recv(10)
        msg_length = int(prefix.decode())
        data = sock.recv(msg_length)
        return data.decode()
    except Exception:
        return None
