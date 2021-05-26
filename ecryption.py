import datetime
import hashlib


# Caesar encryption

# шифрование текста
def encrypt_caesar(msg, k):
    return shift_caesar(msg, k)


# дешифрование текста
def decrypt_caesar(msg, k):
    return shift_caesar(msg, -k)


# функция сдвига символов сообщения msg на key позиций
def shift_caesar(msg, key):
    shifted = []
    for letter in msg:
        shifted.append(chr((ord(letter) + key) % 65536))
    return ''.join(shifted)


# Vigenere encryption

# вспомогательная функция доформирования ключа
def key_vigenere(n, k):
    diff = n - len(k)
    if diff > 0:
        k += (diff // len(k)) * k + k[:diff % len(k)]
    key = []
    for letter in k:
        key.append(int(letter))
    return key


# шифрование текста
def encrypt_vigenere(msg, k):
    if not k.isdigit():
        return "Wrong format of the key"
    return shift_vigenere(msg, key_vigenere(len(msg), k))


# дешифрование текста
def decrypt_vigenere(msg, k):
    if not k.isdigit():
        return "Wrong format of the key"
    return shift_vigenere(msg, [i * (-1) for i in key_vigenere(len(msg), k)])


# функция сдвига символов сообщения msg на key позиций
def shift_vigenere(msg, key):
    shifted = []
    for i, letter in enumerate(msg):
        shifted.append(chr((ord(letter) + key[i]) % 65536))
    return ''.join(shifted)


# OTP (Vernam) generation

def encrypt_otp(msg, key):
    if len(msg) != len(key):
        return "Wrong length"
    result = []
    for i in range(len(msg)):
        key_bin = ''.join(format(ord(key[i]), 'b'))
        msg_bin = ''.join(format(ord(msg[i]), 'b'))
        result.append(int("0b" + ''.join([str(int(msg_bin[j]) ^ int(key_bin[j])) for j in range(7)]), 2))
    return result


# Blockchain

class BlockChain:

    def __init__(self, index, timestamp, msg, last_key):
        self.index = index
        self.timestamp = timestamp
        self.msg = msg
        self.last_key = last_key
        self.key = self.keygen()

    # шифрование и создание блока шифротекста
    def keygen(self):
        sha = hashlib.sha256()
        sha.update((str(self.index) + str(self.timestamp) + str(self.msg) + str(self.last_key)).encode('utf-8'))
        return sha.hexdigest()

# создание следущего блока
def next_block(block):
    index = block.index + 1
    timestamp = datetime.datetime.now()
    msg = "New block " + str(index)
    key = block.key
    return BlockChain(index, timestamp, msg, key)

# создание первого блока
def create_first_block():
    return BlockChain(0, datetime.datetime.now(), "Start chain", "0")


# Feistel network

key = 'Abcdefg'
position = 0

# шифрование текста
def encrypt_festel(msg):
    global position
    if len(msg) % 2 != 0:
        msg = msg + ' '
    result = []
    for i in range(0, len(msg), 2):
        result.append(shift_festel(ord(msg[i]), ord(msg[i + 1]), 1))
    position -= 1
    return ''.join(result)


# дешифрование текста
def decrypt_festel(msg):
    if len(msg) % 2 != 0:
        msg = msg + ' '
    result = []
    for i in range(len(msg) - 1, -1, -2):
        result.insert(0, shift_festel(ord(msg[i - 1]), ord(msg[i]), -1))
    return ''.join(result)


# алгоритм сети Фейстеля
def shift_festel(L, R, pos):
    global position
    for i in range(16):
        k = ord(key[position % len(key)])
        L, R = R ^ (L ^ k), L
        position += pos
    return chr(R) + chr(L)


text = 'What is a wonderful night'

print(text)
s = encrypt_caesar(text, 7)
print(s)
print(decrypt_caesar(s, 7))
print()
print(text)
s = encrypt_vigenere(text, "357689")
print(s)
print(decrypt_vigenere(s, "357689"))
print()
print(text)
s = encrypt_festel(text)
print(s)
print(decrypt_festel(s))
print()
print(encrypt_otp("LONDON", "SYSTEM"))
