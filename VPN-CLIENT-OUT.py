import pydivert
import re
import socket
import sys
import time
import selectors
import socket
import cryptography
from cryptography.fernet import Fernet
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
def CatchPackets():
    print('catching packets')
    w = pydivert.WinDivert("outbound and tcp.DstPort == 8000")
    w.open()
    while True:
        request = w.recv()
        payload = request.payload
        payload = payload.decode('utf-8')
        try:
            try:
                #trying to get rid of accept-encoding thing, cause it compresses data on answer, and i dont know how to handle it;P
                payload = re.sub('\r\nAccept-Encoding:.+\r\n','\r\n',payload)
            except:
                pass
            print(payload.encode('utf-8'))
            payload = encrypt(payload,key)
            payload = payload.encode('utf-8')
            request.payload = payload
            w.send(request)
            #w.close() ### ДЛЯ ТОГО ЧТОБЫ ОНО РАБОТАЛО НА ОДНОЙ И ТОЙ ЖЕ МАШИНЕ НА КОТОРОЙ НАХОДИТСЯ И СЕРВЕР, ПРЕЖДЕ ЧЕМ ОТПРАВЛЯТЬ ЗАПРОСЫ НА ПОРТ 80 НАДО ВЫКЛЮЧИТЬ ПЕРЕХВАТ ЭТИХ ЖЕ ЗАПРОСОВ
        except:
            #если пустой payload это значит что это tcp handshake или что то похожее.
            w.send(request)
CatchPackets()