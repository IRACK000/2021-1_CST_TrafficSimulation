# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : sockets.logclient & Last Modded : 2021.05.05. ###
Coded with Python 3.9 for Windows (CRLF) by IRACK000
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os
import socket

os.system("MODE CON cols=30 lines=40")
os.system("TITLE LOG Recv Client")
HOST = '127.0.0.1'
PORT = 54783
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("Connected!")
while True:
    data = client_socket.recv(1024)
    if not data:  # 빈 문자열을 수신시 루프 탈출.
        break
    print(data.decode(), end='')
client_socket.close()
