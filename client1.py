import pydivert
import re
import socket
import sys
import time
import selectors
import socket
alphabet = 'abcdefghijklmnopqrstuvwxyz'
key = 'zyxwvutsrqpomnlkjihgfedcba'
def decrypt(message,key):
    count = 0
    while True:
        if(count > 25):
            break
        message = re.sub(key[count]+'(?!!)',alphabet[count]+'!',message)
        count = count + 1
    message = message.replace('!','')
    return message
def CatchPackets():
    print('catching packets')
    w = pydivert.WinDivert("inbound and tcp.SrcPort == 8000")
    w.open()
    while True:
        request = w.recv()
        payload = request.payload.decode('utf-8')
        if payload:
            payload = decrypt(payload,key)
            request.payload = payload.encode('utf-8')
            print(request.payload)
            try:
                w.send(request)
            except:
                print('smth error')
            time.sleep(0.1)
        else:
            print('empty payload')
            w.send(request)

CatchPackets()