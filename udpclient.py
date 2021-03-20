import socket


def listen(client, time):
    bufferSize = 1024
    client.settimeout(time)
    try:
        while True:
            answer = client.recvfrom(bufferSize)
            print(answer[0].decode())
    except socket.timeout:
        exit


serverAddressPort = ("127.0.0.1", 9090)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Welcome to chat: ")
while True:
    try:
        listen(client, 1)
        client.settimeout(3)
        try:
            message = input()
            if message != "":
                client.sendto(message.encode(), serverAddressPort)
        except socket.timeout:
            pass
    except KeyboardInterrupt:
        break
client.close()
