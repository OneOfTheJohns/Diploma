import socket
import random
import re
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

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)
def Main():
    while True:    
        # Wait for client connections
        client_connection, client_address = server_socket.accept()
        thread = threading.Thread(target=Work, args=(client_connection, client_address))
        thread.start()
        # Get the client request
def Work(client_connection, client_address):
    payload = client_connection.recv(1024)
    payload = payload.decode('utf-8')
    payload = decrypt(payload,key)
    try:
        #trying to get rid of accept-encoding thing, cause it compresses data on answer, and i dont know how to handle it;P
        payload = re.sub('\r\nAccept-Encoding:.+\r\n','\r\n',payload)
    except:
        pass
    try:
        url = re.findall(r"Host: (.*)",payload)
        url = url[0].split("\r")
        url = url[0]
        f = socket.socket()
        f.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        a = random.randint(2000,9999)
        f.bind(("0.0.0.0", a))
        print(url)
        print(payload)
        f.connect((url,80))
    except:
        pass
    f.sendall(payload.encode('utf-8'))
    count = 0
    while True:
        data = f.recv(2046)
        if data:
            print(data)
            try:
                data = encrypt(data.decode('utf-8'),key).encode('utf-8')
            except:
                print('got image')
            client_connection.sendall(data)
        else:
            count = count + 1
            if count > 5:
                print('count')
                f.close()
                client_connection.close()
                Main()
            pass
Main()
server_socket.close()