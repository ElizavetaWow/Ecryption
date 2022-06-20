import socket
import threading
import sys

def bar(step, n):
    length = 60
    filled = int(round(length * step/n))
    unfilled = length - filled
    view = "*"*filled+"-"*unfilled
    percents = round(100.0 * step/n, 1)
    if step == n - 1:
        dop = '\n'
    else:
        dop = '\r'
    sys.stdout.write(f'[{view}] {percents}%'+dop)
    sys.stdout.flush()



class T(threading.Thread):
    def __init__(self, host, n):
        threading.Thread.__init__(self, name="t" + str(n))
        self.host = host
        self.port = n

    def run(self):
        global soc_list
        sock = socket.socket()
        try:
            sock.connect((self.host, self.port))
            with lock:
                soc_list.append(self.port)
        except:
            pass
        sock.close()

lock = threading.Lock()
n = 2**16 - 1

host = input('Write hostname:')
soc_list = []
threads = [T(host, port) for port in range(1, n)]
for port in range(1, n):
    threads[port - 1].start()
    bar(port, n)
[threads[port - 1].join() for port in range(1, n)]
soc_list.sort()
for port in soc_list:
    print("Порт", port, "открыт")

