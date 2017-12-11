# -*- coding: utf-8 -*-
"""
использует сокеты для обмена данными между заданиями: запускает потоки
выполнения, взаимодействующие с помощью сокетов; независимые программы также
могут использовать сокеты для взаимодействий, потому что они принадлежат
системе в целом, как и именованные каналы; смотрите части книги, посвященные
разработке графических интерфейсов и сценариев для Интернета, где приводятся
более практичные примеры использования сокетов; некоторым серверам может
потребоваться взаимодействовать через сокеты с клиентами в виде потоков
выполнения и процессов; данные через сокеты передаются в виде строк байтов, но
точно так же через них можно передавать сериализованные объекты или кодированный
текст Юникода;
ВНИМАНИЕ: при обращении к функции print в потоках выполнения может потребоваться
синхронизировать их, если есть вероятность перекрытия по времени;
"""
from socket import socket, AF_INET, SOCK_STREAM # переносимый API сокетов
port = 50008 # номер порта, идентифицирующий сокет
host = 'localhost' # сервер и клиент выполняются на локальном компьютере

def server():
    sock = socket(AF_INET, SOCK_STREAM) # IP-адрес TCP-соединения
    sock.bind(('', port)) # подключить к порту на этой машине
    sock.listen(5) # до 5 ожидающих клиентов

    while True:
        conn, addr = sock.accept() # ждать соединения с клиентом
        data = conn.recv(1024) # прочитать байты данных от клиента
        reply = 'server got: [%s]' % data # conn - новый подключенный сокет
        conn.send(reply.encode()) # отправить байты данных клиенту

def client(name):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port)) # подключить сокет к порту
    sock.send(name.encode()) # отправить байты данных серверу
    sock.send(name.encode())  # отправить байты данных серверу
    reply = sock.recv(1024) # принять байты данных от сервера
    sock.close() # до 1024 байтов в сообщении
    print('client got: [%s]' % reply)

if __name__ == '__main__':
    from threading import Thread
    sthread = Thread(target=server)
    sthread.daemon = True # не ждать завершения потока сервера
    sthread.start() # ждать завершения дочерних потоков
    for i in range(5):
        Thread(target=client, args=('client%s' % i,)).start()