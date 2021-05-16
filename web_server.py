import socket

sock = socket.socket() #создание сокета
try: #назначение хоста и порта сокету
    sock.bind(('', 80))
    print("Using port 80")
except OSError:
    sock.bind(('', 8080))
    print("Using port 8080")
sock.listen(5)

while True:
    try:
        conn, addr = sock.accept() #ожидание подключения

        data = conn.recv(8192).decode() #отображение запроса от клиента
        print(data)

        file = open('index.html') #отображение начальной страницы
        page = file.read()
        file.close()

        #создание и отправка ответа клиенту
        resp = """HTTP/1.1 200 OK
        Server: SelfMadeServer v0.0.1
        Content-type: text/html
        Connection: close\n\n""" + page
        conn.sendall(resp.encode())
        conn.close()
    except:
      print("Close connection")
      break

sock.close() #закрытие сокета
