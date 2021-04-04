import socket
from threading import Thread

n = 2**16 - 1
host = input('Write hostname:')

for port in range(1, n):
    sock = socket.socket()
    try:
        sock.connect((host, port))
        print("Порт", port, "открыт")
    except:
        continue
    finally:
        sock.close()