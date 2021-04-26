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
        url = GetUrl(client_connection, client_address)
        data = GetRequest(url)
        data = data.decode('utf-8')
        #data = 'HTTP/1.0 200 OK\n\nHello World'
        #data = data.encode('utf-8')
        #response = data
        #data = data[:1400]
        print(data)
        #Removing Transfer-encoding chuncked , if there is.
        response = encrypt(data,key)
        response = response.encode('utf-8')
        print('sending page back to client')
        #print(response)
        while True:
            client_connection.send(response)
            break
            #client_connection.sendall(b'end')
            #client_connection.close()
            #sys.exit()
def GetUrl(client_connection, client_address):
    while True:
        url = client_connection.recv(1042)
        url = url.decode('utf-8')
        url = decrypt(url,key)
        print(url)
        break
    return url
def GetRequest(url):
    full_data = ''
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
    f.connect((url, 80))
    url2 = url.encode('utf-8')
    f.sendall(b"GET / HTTP/1.1\r\nHost:"+url2+b"\r\n\r\n")
    while True:
        try:
            data = f.recv(4096)
            if len(data) > 0:
                print('got some data, appending')
                data = data.decode('utf-8')
                full_data = full_data + data
            else:
                print('received all data ending')
                break
        except:
            print('Got all data')
            break
    #print(full_data)
    data = full_data.encode('utf-8')
    f.setblocking(False)
    f.close()
    return data
main()
    #server_socket.close()

# https://www.codementor.io/@joaojonesventura/building-a-basic-http-server-from-scratch-in-python-1cedkg0842
# %LocalAppData%\Google\Chrome\User Data\Default\Cache --- google chrome cache
# https://github.com/ffalcinelli/pydivert
# https://realpython.com/python-sockets/
# https://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password
# https://ru.wikipedia.org/wiki/Transmission_Control_Protocol
# https://tools.ietf.org/html/rfc2616#section-4.4
# https://tools.ietf.org/html/rfc7230#section-3.3.3