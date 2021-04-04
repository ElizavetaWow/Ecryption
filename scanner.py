import socket
import threading

class T(threading.Thread):
    def __init__(self, host, n):
        threading.Thread.__init__(self, name="t" + str(n))
        self.host = host
        self.port = n

    def run(self):
        sock = socket.socket()
        try:
            sock.connect((self.host, self.port))
            print("Порт", self.port, "открыт")
        except:
            pass
        sock.close()

n = 2**16 - 1
host = input('Write hostname:')

for port in range(1, n):
    sock = socket.socket()
    p = T(host, port)
    p.start()
