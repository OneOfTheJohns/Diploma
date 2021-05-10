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
        #Failed to load resource: net::ERR_CONTENT_LENGTH_MISMATCH
        #try to get page lenght and insert this number into header?
        payload = request.payload
        print(payload)
        try:
            payload = payload.decode('utf-8')
            payload = decrypt(payload,key)
            #print(payload)
            payload = payload.encode('utf-8')
            if payload:
                # payload_header = payload.split('\r\n\r\n')[0]
                # payload_data = payload.split('\r\n\r\n')[1]
                # payload_data_len = len(payload_data)
                # new_payload_header = re.sub('Content-Length: [0-9]+','Content-Length:'+str(payload_data_len),payload_header)
                # payload = new_payload_header + '\r\n\r\n' + payload_data
                # request.payload = b'HTTP/1.0 200 OK\n\nHello World'
                request.payload = payload
                #print(request.payload)
                w.send(request)
                time.sleep(0.01)
            else:
                w.send(request)
        except:
            print(payload)
            w.send(request)
            time.sleep(0.01)

CatchPackets()