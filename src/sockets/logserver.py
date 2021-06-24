# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : sockets.logserver & Last Modded : 2021.05.05. ###
Coded with Python 3.9 for Windows (CRLF) by IRACK000
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os
import platform
import socket  # https://webnautes.tistory.com/1381

logging: bool = False
logging_level: int = 1


def open(show):
    if show:
        print("Logging: ON")
    HOST = '127.0.0.1'  # localhost
    PORT = 54783  # 1~65535
    global server_socket  # 서버 소켓 생성. (IPv4, TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # to fix WinError 10048.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))  # 커널에 바인드.
    if show:
        print("Open Log Recv Client")
    command: str = "start "
    if platform.system() == "Darwin":  # 맥에서 작동 확인 안해봤음.
        command = "open python3 "
    os.system(command
              + os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
              + "/sockets/logclient.py"
              )
    server_socket.listen()  # 접속 대기.
    global client_socket, addr
    client_socket, addr = server_socket.accept()  # 클라이언트 소켓 리턴.
    if show:
        print('Connected by', addr)  # 접속한 클라이언트 주소.
    global logging
    logging = True


def close():
    global server_socket
    global logging
    logging = False
    client_socket.close()
    server_socket.close()


def on(show=False):
    if not logging:
        open(show)


def off():
    if logging:
        close()


def setlevel(level):
    """1 : normal, 2 : not necessary, 3 : too deep"""
    global logging_level
    logging_level = level


def send(txt, level=1):
    if type(txt) is not str:
        txt = str(txt)
    if logging and level <= logging_level:
        txt += '\n'
        client_socket.sendall(txt.encode())
