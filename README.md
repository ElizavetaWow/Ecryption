# Простейшие TCP-клиент и эхо-сервер

## Основное задание
1. Создать простой TCP-сервер, который принимает от клиента строку порциями по 1 КБ и возвращает ее. (Эхо-сервер).
2. Сервер должен выводить в консоль служебные сообщения с пояснениями при наступлении любых событий:
    + Запуск сервера;
    + Начало прослушивания порта;
    + Подключение клиента;
    + Прием данных от клиента;
    + Отправка данных клиенту;
    + Отключение клиента;
    + Остановка сервера.
3. Написать простой TCP-клиент, который устанавливает соединение с сервером, считывает строку со стандартного ввода и посылает его серверу.
4. Клиент должен выводить в консоль служебные сообщения с пояснениями при наступлении любых событий:
    + Соединение с сервером;
    + Разрыв соединения с сервером;
    + Отправка данных серверу;
    + Прием данных от сервера.

## Дополнительное задание
1. Проверить возможность подключения к серверу с локальной, виртуальной и удаленной машины.
2. Модифицировать код сервера таким образом, чтобы он читал строки в цикле до тех пор, пока клиент не введет “exit”.
3. Модифицировать код сервера таким образом, чтобы при разрыве соединения клиентом он продолжал слушать данный порт и был доступен для повторного подключения.
4. Модифицировать код клиента и сервера таким образом, чтобы номер порта и имя хоста для клиента они спрашивали у пользователя. Реализовать безопасный ввод данных и значения по умолчанию.
5. Модифицировать код сервера таким образом, чтобы все служебные сообщения выводились не в консоль, а в специальный лог-файл.
6. Модифицировать код сервера таким образом, чтобы он автоматически изменял номер порта, если он уже занят. Сервер должен выводить в консоль номер порта, который он слушает.
7. Реализовать сервер идентификации. Сервер должен принимать соединения от клиента и проверять, известен ли ему уже этот клиент (по IP-адресу). Если известен, то поприветствовать его по имени. Если неизвестен, то запросить у пользователя имя и записать его в файл. Файл хранить в произвольном формате.
8. Реализовать сервер аутентификации. Похоже на предыдущее задание, но вместе с именем пользователя сервер отслеживает и проверяет пароли.
9. Реализовать вспомогательные функции, которые реализуют отправку и принятие текстовых сообщений в сокет. Функция отправки должна дополнять сообщение заголовком фиксированной длины, в котором содержится информация о длине сообщения. Функция принятия должна читать сообщение с учетом заголовка. В дополнении реализуйте преобразование строки в байтовый массив и обратно в этих же функциях.
10. Дополнить код клиента и сервера таким образом, чтобы они могли посылать друг другу множественные сообщения один в ответ на другое.
11. Написать многопользовательский чат, использовать сокеты, основанные на протоколе UDP.
