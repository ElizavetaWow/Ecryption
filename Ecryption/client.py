import socket
import random
import math
from Crypto import PublicKey
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
import hashlib

# создание сокета
sock = socket.socket()

while True:
    # подключение к серверу
    sock.connect(('localhost', 8080))

    # авторизация на сервере
    idd = input("Введите логин: ")
    sock.send(idd.encode())
    # получение ответа от сервера и ввод пароля
    data = sock.recv(1024)
    password = input("Введите пароль: ")

    # создание ключа шифрования из пароля
    key = hashlib.sha256(password.encode()).digest()
    IV = 16 * '\x00'
    encryptor = AES.new(key, AES.MODE_CFB, IV)
    resp = encryptor.encrypt(data)
    # Отправление ответа на сервер
    sock.send(resp)
    data = sock.recv(1024)
    # получен ответ о том, правильный ли был введён пароль. Если нет, соединение с сервером прерывается
    if data == "Неверный пароль!":
        break

    # генерация ключа сессии
    g = 5
    p = 23
    sock.send(str(g).encode())
    sock.send(str(p).encode())

    # создание секретной части а
    a = 6
    print("Секретное значение а:" + str(a))
    A = (g ** a) % p
    sock.send(str(A).encode())
    hashA = hashlib.sha256(str(A).encode()).digest()

    with open("publickey1.pem", "r") as f:
        RSAkey1 = RSA.import_key(f.read())

    # раскодирование данных из файла с публичным ключом
    signA = RSAkey1.encode().encrypt(hashA, 32)
    sock.send(signA[0])
    print("g:".encode() + str(g).encode())
    print("p:".encode() + str(p).encode())
    print("A:".encode() + str(A).encode())
    print("signA:".encode() + signA[0])
    print("Данные отправлены серверу".encode())

    # извлекаем второй приватный ключ
    with open("privatekey2.pem", "r") as f:
        RSAkey2 = f.read()
    RSAkey2 = RSA.importKey(RSAkey2)

    # Секретное значение B для ключа сессии получено от сервера
    B = sock.recv(1024)
    signB = sock.recv(1024)
    print("Значение b получено".encode())
    print("B:".encode() + str(B).encode())
    print("signB".encode() + signB)

    # Проверка значений
    hashB = hashlib.sha256(B).digest()
    checkHash = RSAkey2.decrypt(signB)
    print("hashB:".encode() + hashB)
    print("CheckHashB:".encode() + checkHash)

    if hashB == checkHash:
        print("Проверка пройдена успешно!".encode())

        # Так сервер отправил правильное секретное значение, можно сгенерировать ключ сессии
        sessionKey = str((int(B) ** a) % p)
        print("Ключ сессии сгенерирован успешно:".encode() + sessionKey)
    else:
        print("Проверка хэша не пройдена, невозможно сгенерировать ключ сессии!".encode())
        break

    # Получаем зашифрованный файл от сервера. Используем ключ сессии для его расшифровки и чтения
    encryptedEMR = sock.recv(1024)
    print("Файл получен".encode())

    # расшифровка
    sessionKey = hashlib.sha256(sessionKey).digest()
    decryptor = AES.new(sessionKey, AES.MODE_CFB, IV)
    decryptedEMR = decryptor.decrypt(encryptedEMR)
    print("Decrypted EMR:".encode() + decryptedEMR)
    break
