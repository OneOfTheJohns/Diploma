import pydivert
import re
import socket
import sys
import time
import selectors
import socket
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 7774      # The port used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
def SendUrlToServer():
    s.sendall(url)
    ListenForAnswer()

def CatchPackets():
    global url
    while True:
        w = pydivert.WinDivert("tcp.DstPort == 80 and tcp.PayloadLength > 0")
        w.open()
        request = w.recv()

        print("catching packets")
        #print(request)
        payload = request.payload
        payload = payload.decode("utf-8")
        #print(payload)
        url = re.findall(r"Host: (.*)",payload)
        if url:
            url = url[0].split("\r")
            url = url[0]
            url = url.encode("utf-8")
            print('printing url')
            print(url)
            w.close() ### ДЛЯ ТОГО ЧТОБЫ ОНО РАБОТАЛО НА ОДНОЙ И ТОЙ ЖЕ МАШИНЕ НА КОТОРОЙ НАХОДИТСЯ И СЕРВЕР, ПРЕЖДЕ ЧЕМ ОТПРАВЛЯТЬ ЗАПРОСЫ НА ПОРТ 80 НАДО ВЫКЛЮЧИТЬ ПЕРЕХВАТ ЭТИХ ЖЕ ЗАПРОСОВ
            SendUrlToServer()
        else:
            print("payload is empty")

def ListenForAnswer():
    while True:
        data = s.recv(4096)
        if data:
            data2 = data.decode('utf-8')
            print(data2)
            break

CatchPackets()