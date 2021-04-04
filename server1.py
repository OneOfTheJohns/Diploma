import socket
import requests
import urllib
import sys
import re
import selectors
import time
import random
import socket
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 7774      # The port used by the server

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen()
conn, addr = s.accept()
s.setblocking(False)
print('Connected by', addr)
print("listening")
def GetUrlFromClient():
    global url
    while True:
        while True:
            url = conn.recv(1024)
            if url:
                url = url.decode('utf-8')
                print(url)
                break
        GetRequest()
def GetRequest():
    global data
    f = socket.socket()
    f.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        a = random.randint(2000,9999)
        f.bind(("0.0.0.0", a))
    except:
        a = random.randint(2000,9999)
        f.bind(("0.0.0.0", a))
    f.connect((url, 80))
    url2 = url.encode('utf-8')
    f.sendall(b"GET / HTTP/1.1\r\nHost:"+url2+b"\r\n\r\n")
    data = f.recv(4096)
    f.setblocking(False)
    data2 = data.decode('utf-8')
    #print(data2)
    f.close()
    SendAnswerToClient()

def SendAnswerToClient():
    conn.sendall(data)
    GetUrlFromClient()

GetUrlFromClient()