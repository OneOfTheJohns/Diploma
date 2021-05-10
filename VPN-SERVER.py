import socket
import requests
import urllib
import sys
import re
import selectors
import time
import random
import socket
import threading

#Connection for web browser (tcp handshake)
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000
alphabet = 'abcdefghijklmnopqrstuvwxyz'
key = 'zyxwvutsrqpomnlkjihgfedcba'
def encrypt(message,key):
    count = 0
    while True:
        if(count > 25):
            break
        message = re.sub(alphabet[count]+'(?!!)',key[count]+'!',message)
        count = count + 1
    message = message.replace('!','')
    return message
def decrypt(message,key):
    count = 0
    while True:
        if(count > 25):
            break
        message = re.sub(key[count]+'(?!!)',alphabet[count]+'!',message)
        count = count + 1
    message = message.replace('!','')
    return message
def main():
    global client_connection
    global server_socket
    global thread
    print('HostingSocket')
    #Making this shit to work with tcp handshakes
    #basicly handshaking with client
    #Connection for page (html) transporting (from server to client)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    # Wait for client connections
    while True:
        client_connection, client_address = server_socket.accept()
        thread = threading.Thread(target=Response, args=(client_connection, client_address))
        thread.start()
def Response(client_connection, client_address):
    while True:    
        # Get the client request
        payload = GetUrl(client_connection, client_address)
        payload2 = payload.decode('utf-8')
        #print(payload2)
        #
        #проблема - пустые запросы или запросы определённых байтов от клиента, не уходят в интернет, т.к подключение создаётся в 1 thread, а пустой запрос уже в другом thread
        #
        try:
            url = re.findall(r"Host: (.*)",payload2)
            url = url[0].split("\r")
            url = url[0]
            GetRequest(payload,url)
        except:
            break
def GetUrl(client_connection, client_address):
    while True:
        payload = client_connection.recv(1042)
        payload = payload.decode('utf-8')
        #payload = decrypt(payload,key)
        payload = payload.encode('utf-8')
        break
    return payload
def GetRequest(payload,url):
    #making http request to received url, and getting page as answer
    #
    #Request module dosnt work with long urls? --- like (ipv6.tlund.se)
    #
    print('getting request')
    global data
    f = socket.socket()
    f.settimeout(1)
    f.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        a = random.randint(2000,9999)
        f.bind(("0.0.0.0", a))
    except:
        a = random.randint(2000,9999)
        f.bind(("0.0.0.0", a))
    #print(url)
    #print(payload)
    #
    #может быть сделано через pydivert? перехват пакета отправляемого клиентом - замена payload, dst.ip, src.ip?
    #
    f.connect((url, 80))
    # url2 = url.encode('utf-8')
    # f.sendall(b"GET / HTTP/1.1\r\nHost:"+url2+b"\r\n\r\n")
    print(payload)
    f.sendall(payload)
    while True:
        try:
            data = f.recv(1024)
            print(data)
            try:
                data = data.decode('utf-8')
                #data = encrypt(data,key)
                data = data.encode('utf-8')
            except:
                pass
        except:
            break
        client_connection.send(data)
    f.setblocking(False)
    f.close()
main()

# https://www.codementor.io/@joaojonesventura/building-a-basic-http-server-from-scratch-in-python-1cedkg0842
# %LocalAppData%\Google\Chrome\User Data\Default\Cache --- google chrome cache
# https://github.com/ffalcinelli/pydivert
# https://realpython.com/python-sockets/
# https://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password
# https://ru.wikipedia.org/wiki/Transmission_Control_Protocol
# https://tools.ietf.org/html/rfc2616#section-4.4
# https://tools.ietf.org/html/rfc7230#section-3.3.3