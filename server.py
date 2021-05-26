import socket
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
import hashlib

# Создание сокета и его привязка
sock = socket.socket()
sock.bind(('localhost', 8080))
sock.listen(5)

while True:
    # подключение клиента и получение его данных
    conn, addr = sock.accept()
    print("Подсоединён " + addr[0])
    data = conn.recv(1024)
    opk = Random.new().read(16)
    conn.send(opk)

    # задаём пароль для входа и создаём хэш
    password = "password"
    hash_key = hashlib.sha256(password.encode()).digest()
    IV = 16 * '\x00'
    # создаём ключ расшифровки
    decypher = AES.new(hash_key, AES.MODE_CFB, IV)

    # получение открытого ключа от клиента
    resp = conn.recv(1024)

    # проверка ключа
    if decypher.decrypt(resp) == opk:
        conn.send("Здравствуйте!".encode())
    else:
        conn.send("Неверный пароль!".encode())
        break

    # генерация кдюча сессии
    g = conn.recv(1024)
    p = conn.recv(1024)
    A = conn.recv(1024)
    signA = conn.recv(1024)
    print("Получены ключи от клиента:".encode())
    print("g:".encode() + str(g).encode())
    print("p:".encode() + str(p).encode())
    print("A:".encode() + str(A).encode())
    print("signA:".encode() + signA)

    # получение ключей из специально подготовленного файла
    with open("privatekey1.pem", "r") as f:
        RSAkey1 = f.read()
    RSAkey1 = RSA.importKey(RSAkey1)
    checkHashA = RSAkey1.decrypt(signA)
    hashA = hashlib.sha256(A).digest()

    with open("privatekey2.pem", "r") as f:
        RSAkey2 = f.read()
    RSAkey2 = RSA.importKey(RSAkey2)
    print("хэш А:" + hashA)
    print("Проверка хэш А:" + checkHashA)

    # производится проверка контрольной суммы
    if hashA == checkHashA:
        print("Проверка пройдена успешно!")
        b = 15
        B = (int(g) ** b) % int(p)
        print("Секретное значение b:" + str(b))

        hashB = hashlib.sha256(str(B)).digest()
        signB = RSAkey2.encrypt(hashB, 32)
        # секретное значение отправляется пользователю и генерируется ключ
        conn.send(str(B))
        conn.send(signB[0])
        print("B:" + str(B))
        print("signB:" + signB[0])
        print("Данные отправлены клиенту")

        sessionKey = str((int(A) ** b) % int(p))
        print("Ключ сессии сгенерирован успешно:" + sessionKey)
    else:
        print("Проверка хэша не пройдена, невозможно сгенерировать ключ сессии!")
        break

    # открываем файл, по ключу сессии зашифровываем содержимое и отправляем его клиенту
    with open("EMR.txt", "r") as f:
        EMRfile = f.read()

    sessionKey = hashlib.sha256(sessionKey).digest()
    # ключ шифрования
    encryptor = AES.new(sessionKey, AES.MODE_CFB, IV)

    encryptedEMR = encryptor.encrypt(EMRfile)

    conn.send(encryptedEMR)
    print("EMR отправлено клиенту")
    print("Зашифрованный файл:" + encryptedEMR)
    break

conn.close()
sock.close()
