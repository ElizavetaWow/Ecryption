#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import threading
import json
from commonFuncs import *
import os
import LinMng
import WinMng
import platform

class User(threading.Thread): #класс потока пользователя
    def __init__(self, conn, addr):
        threading.Thread.__init__(self, name=str(addr[0]) + " " + str(addr[1]))
        self.host = addr[0]
        self.port = addr[1]
        self.conn = conn
        self.dir = ""

    def run(self):
        try:
            if self.authentication(): #аутентификация и принятие запросов
                while True:
                    data = getP(self.conn)
                    sendP(self.conn, self.process(data))
                    if data == "exit":
                        break
        except KeyboardInterrupt as k:
            with lock2:
                with open(os.path.join(main_path, 'log.txt'), 'a') as log:
                    log.write(k)
        except ConnectionResetError:
            with lock2:
                with open(os.path.join(main_path, 'log.txt'), 'a') as log:
                    log.write("Lost connection from client\n")
        with lock2:
            with open(os.path.join(main_path, 'log.txt'), 'a') as log:
                log.write('Server stops connection with ' + str(self.host) + " " + str(self.port) + '\n')
        self.conn.close()

    def process(self, req): #обработка запросов через менеджеры
        menuList = ["create", "delete", "ls", "pwd", "cp", "renamef", "change", "exit", "help"]
        try:
            command = req.split()
            if not(command[0].lower() in menuList):
                return 'bad request'
        except:
            return 'bad request'
        commandIndex = menuList.index(command[0])
        if commandIndex == 0:
            return self.manager.create(command[1:])
        if commandIndex == 1:
            return self.manager.delete(command[1:])
        if commandIndex == 2:
            return self.manager.print_content()
        if commandIndex == 3:
            return self.manager.print_path()
        if commandIndex == 4:
            return self.manager.copy(command[1:])
        if commandIndex == 5:
            return self.manager.rename(command[1:])
        if commandIndex == 6:
            return self.manager.change_directory(command[1:])
        if commandIndex == 7:
            return 'exit'
        if commandIndex == 8:
            return print_instractions()



    def authentication(self): #функция аутентификации
        with lock:
            with open(os.path.join(main_path, 'clients.json'), 'r') as cl:
                client_dict = json.load(cl)
            key = str(self.host) + "_" + str(self.port)
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
                    if platformName == "Windows":
                        self.manager = WinMng.WinMng(self.dir)
                    if platformName == "Linux":
                        self.manager = LinMng.LinMng(self.dir)
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
                    self.dir = os.path.join(path, key)
                    if platformName == "Windows":
                        os.makedirs(self.dir)
                        self.manager = WinMng.WinMng(self.dir)
                    if platformName == "Linux":
                        os.system('mkdir ' + self.dir)
                        self.manager = LinMng.LinMng(self.dir)

                    sendP(self.conn, "Registration completed")
            with open(os.path.join(main_path, 'clients.json'), 'w') as cl:
                json.dump(client_dict, cl)
        return result


def print_instractions():
    comands  = {"create type name":"Создание файла (type = \"-f\") или директории (type = \"-d\") с названием name",
                "delete type name":"Удаление файла (type = \"-f\") или директории (type = \"-d\") с названием name",
                "renamef \"lastname\" \"newname\"":"Переименование файла или директории с именем lastname на newname (двойные кавычки обязательны)",
                "change newplace":"Переход в директорию с именем newplace или на уровень выше, если newplace = \"..\"",
                "cp \"lastplace\" \"newplace\"":"Копирование файла с именем lastname в директорию с именем newplace (двойные кавычки обязательны)",
                "ls":"Содержимое текущей директории",
                "pwd": "Текущий путь",
                "exit":"Завешение работы",
                "help":"Вызов справки по командам"}
    i = 1
    for k, v in comands.items():
        print(i, ') ', k, ' - ', v)
        i += 1


platformName = platform.system() #определение ОС
main_path = "D:\\ftp\\" #папка сервера
path = "D:\\ftp\\users\\" #папка пользователей, у каждого ограничение собственной директорией



lock = threading.Lock()
lock2 = threading.Lock()
try:
    open(os.path.join(main_path, 'clients.json'), 'r') #список пользователей
except FileNotFoundError as e:
    with open(os.path.join(main_path, 'clients.json'), 'w') as cl:
        client_dict = dict()
        json.dump(client_dict, cl)
users = list()
with open(os.path.join(main_path, 'log.txt'), 'a') as log: #логирование
    log.write('Server starts working\n')
sock = createSock()
try:
    with open(os.path.join(main_path, 'log.txt'), 'a') as log:
        log.write('Server\'s socket is ' + str(sock.getsockname()[1]) + '\n')
    while True:
        sock.listen(0)
        conn, addr = sock.accept()
        users.append(User(conn, addr)) #работа с пользователями через потоки
        with open(os.path.join(main_path, 'log.txt'), 'a') as log:
            log.write('Connection established:' + str(addr) + '\n')
        users[-1].start()
        for u in users:
            if not u.is_alive():
                users.remove(u)
except KeyboardInterrupt as k:
    with open(os.path.join(main_path, 'log.txt'), 'a') as log:
        log.write(k)
except ConnectionResetError:
    with open(os.path.join(main_path, 'log.txt'), 'a') as log:
        log.write("Lost connection from client\n")
with open(os.path.join(main_path, 'log.txt'), 'a') as log:
    log.write('Server stops working\n')
sock.close()
