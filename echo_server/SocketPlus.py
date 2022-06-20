import socket


class SocketPlus(socket.socket):

    def __init__(self, head_length=10):
        super().__init__()
        self.head_length = head_length

    def sendP(self, data):
        prefix = str(len(data)).zfill(self.head_length)
        self.send((prefix + data).encode())

    def getP(self):
        try:
            prefix = self.recv(10)
            msg_length = int(prefix.decode())
            data = self.recv(msg_length)
            return data.decode()
        except Exception:
            return None
