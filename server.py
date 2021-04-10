#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import threading


class T(threading.Thread):
    def __init__(self, conn, addr, n):
        threading.Thread.__init__(self, name="t" + str(n))
        self.addr = addr
        self.conn = conn

    def run(self):
        msg = ''
        while True:
            data = self.conn.recv(1024)
            if not data:
                break
            msg += data.decode()
            self.conn.send(data)
        print(msg)
        self.conn.close()


sock = socket.socket()
sock.bind(('localhost', 9090))
sock.listen(0)
n = 1
while True:
    conn, addr = sock.accept()
    print(addr)
    p = T(conn, addr, n)
    p.start()
    n += 1
