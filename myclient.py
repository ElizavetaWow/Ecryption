#!/usr/bin/env python
# -*- coding: utf-8 -*-
import SocketPlus
# Напишите вспомогательные функции, которые реализуют отправку и принятие текстовых сообщений в сокет.
# Функция отправки должна дополнять сообщение заголовком фиксированной длины, в котором содержится информация о длине сообщения.
# Функция принятия должна читать сообщение с учетом заголовка. В дополнении реализуйте преобразование строки в байтовый массив и
# обратно в этих же функциях.
# Дополнително оценивается, если эти функции будут реализованы как унаследованное расширение класса socket библиотеки socket.

def getAddress():
    host = input('Write hostname:')
    socket_number = input('Write socket:')
    if not host:
        host = 'localhost'
    if not socket_number or not socket_number.isdigit():
        socket_number = 1025
    else:
        socket_number = int(socket_number)
    return host, socket_number

sock = SocketPlus.SocketPlus()

try:
    host, socket_number = getAddress()
    print(f'Connecting to server on port {host}, {socket_number}')
    sock.connect((host, socket_number))
    print('Connection established')

    data = sock.getP()
    if not data:
        raise Exception
    print(data)
    if 'Hello, what is your name?' in data:
        name = input()
        if not name:
            raise Exception
        sock.sendP(name)

    msg = "start"
    while True:
        msg = input('Write message to server\n')
        if not msg:
            break
        sock.sendP(msg)
        data = sock.getP()
        if not data:
            break
        print(data)
    print('End connection with server')

except KeyboardInterrupt as k:
    print(k)
except ConnectionRefusedError:
    print("Connection refused")
except Exception as s:
    print(s)
finally:
    sock.close()