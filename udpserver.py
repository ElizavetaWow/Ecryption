import socket

host = "127.0.0.1"
port = 9090
addr = (host, port)
bufferSize = 1024
timeout = 600
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(addr)
print("UDP server up and listening")
listClients = list()

while True:
    try:
        print(f'Waiting for data ({timeout} seconds)...')
        server.settimeout(timeout)
        try:
            message, address = server.recvfrom(bufferSize)
            if listClients.count(address) == 0:
                listClients.append(address)
        except socket.timeout:
            print(f'Time is out. {timeout} seconds have passed')
            break
        answer = f"Message [{address[0]}:{address[1]}]:{message.decode()}"
        print(answer)
        for adr in listClients:
            if adr != address:
                server.sendto(answer.encode(), adr)
    except KeyboardInterrupt as k:
        print(k)
        break

server.close()
