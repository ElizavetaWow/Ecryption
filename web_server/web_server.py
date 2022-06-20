import socket
import threading
from datetime import datetime
from time import mktime
from wsgiref.handlers import format_date_time


class User(threading.Thread):  # класс потока пользователя
    def __init__(self, conn, addr):
        threading.Thread.__init__(self, name=str(addr[0]) + " " + str(addr[1]))
        self.host = addr[0]
        self.port = addr[1]
        self.conn = conn

    def run(self):
        # отображение запроса от клиента
        request = self.conn.recv(DATA_SIZE).decode()
        if request != '':
            print(request)
            # отображение нужной страницы
            headers = request.split('\n')
            page = headers[0].split()[1]
            if page == '/':
                page = '/index.html'
            elif '.' not in page:
                page += '.html'

            if page.split('.')[-1] in FILE_FORMATS:
                try:
                    try:
                        with open(SERVER_FOLDER + page, 'r') as file:
                            page_content = file.read()
                        response = """HTTP/1.1 200 OK
                                Server: SelfMadeServer v0.0.1
                                Content-type: text/html
                                Content-length: 5000
                                Date: """ + format_date_time(mktime(datetime.now().timetuple())) + """
                                Connection: close\n\n""" + page_content
                    except UnicodeDecodeError: #для работы с картинками (бинарный тип данных)
                        with open(SERVER_FOLDER + page, 'rb') as file:
                            page_content = file.read()
                        response = """HTTP/1.1 200 OK
                                Server: SelfMadeServer v0.0.1
                                Content-type: image/png
                                Content-length: 5000
                                Date: """ + format_date_time(mktime(datetime.now().timetuple())) + """
                                Connection: close\n\n"""
                    with lock:
                        with open('log.txt', 'a+') as log:
                            log.write(str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")) + ' - ' + self.host
                                      + ' - ' + page + ' - None\n')
                except FileNotFoundError:
                    response = 'HTTP/1.0 404 NOT FOUND\n\nPage Not Found!'
                    with lock:
                        with open('log.txt', 'a+') as log:
                            log.write(str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")) + ' - ' +
                                      self.host + ' - ' + page + ' - 404\n')
            else:
                if page.split('.')[-1] != "ico":
                    response = 'HTTP/1.0 403 FORBIDDEN\n\nForbidden file type!'
                    with lock:
                        with open('log.txt', 'a+') as log:
                            log.write(str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")) + ' - ' +
                                      self.host + ' - ' + page + ' - 403\n')
            if "Content-type: image/png" in response:
                self.conn.sendall(response.encode()+page_content)
            else:
                self.conn.sendall(response.encode())
        self.conn.close()


# получение настроек из файла
with open('settings.txt', 'r') as settings_file:
    settings = {}
    for i in settings_file.readlines():
        settings[i.split("=")[0]] = i.split("=")[1]
SERVER_HOST = settings['SERVER_HOST'].strip()
SERVER_PORT = int(settings['SERVER_PORT'])
DATA_SIZE = int(settings['DATA_SIZE'])
SERVER_FOLDER = settings['SERVER_FOLDER'].strip()
FILE_FORMATS = ['html', 'jpg', 'png', 'js']
# создание сокета
sock = socket.socket()
sock.bind((SERVER_HOST, SERVER_PORT))
sock.listen(5)
lock = threading.Lock()
users = list()
while True:
    try:
        conn, addr = sock.accept()  # ожидание подключения
        users.append(User(conn, addr))  # работа с пользователями через потоки
        users[-1].start()
        for u in users:
            if not u.is_alive():
                users.remove(u)  # убираем закрывшиеся потоки
    except:
        break

# закрытие сокета
sock.close()
