# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : console.keyboard & Last Modded : 2021.05.05. ###
Coded with Python 3.9 for Windows (CRLF) by IRACK000
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from console.util import ConsoleAPI
import console.showboard as sb
import sockets.logserver as log

from multiprocessing import Process, Queue  # https://monkey3199.github.io/develop/python/2018/12/04/python-pararrel.html


class Buffered_ConsoleAPI(ConsoleAPI):
    __buffer = []
    __process = None
    __mutex = False
    __stop_process = False

    @classmethod
    def _watchdog(cls, id, getch, buffer):
        while not cls.__stop_process:
            c = getch()
            if type(c) != str:
                c = c.decode('utf-8')
            if c == '\003':
                raise KeyboardInterrupt
            buffer.append(c)

    @classmethod
    def runprocess(cls):
        if cls.__process is None:
            cls.__process = Process(target=cls._watchdog, args=(
                2, cls.getch, cls.__buffer
            ))
        cls.__process.start()
        log.send("Keyboard Process started", 2)

    @classmethod
    def stopprocess(cls):
        cls.__stop_process = True
        print("\u001B[6n", end='', flush=True)
        cls.__process.join()
        while True:
            c = cls.getch()
            if type(c) != str:
                c = c.decode('utf-8')
            if c == 'R':
                break
        log.send("Keyboard Process stoped", 2)

    @classmethod
    def buf_getch(cls):
        if cls.__mutex:
            return "Locked"
        cls.__mutex = True
        if len(cls.__buffer) != 0:
            c = cls.__buffer.pop(0)
            cls.__mutex = False
            return c
        else:
            cls.__mutex = False
            return None

    @classmethod
    def wrisxy(cls):
        """get console cursor position. {'x': x, 'y': y}"""
        if not cls.__unicode:
            return super().wrisxy()
        while cls.__mutex:
            pass
        cls.__mutex = True
        index = len(cls.__buffer)
        print("\u001B[6n", end='', flush=True)
        get = []
        while True:
            try:
                c = cls.__buffer.pop(index)
            except Exception:
                break
            if c == 'R':
                x = int(''.join(get))
                break
            elif c == ';':
                y = int(''.join(get))
                get.clear()
            elif c >= '0' and c <= '9':
                get.append(c)
        cls.__mutex = False
        return {'x': x, 'y': y}

    @classmethod
    def pause(cls, prompt="Press any key to continue . . ."):
        """pause console"""
        # 참고 : https://stackoverflow.com/questions/493386/how-to-print-without-newline-or-space
        print(prompt, end='', flush=True)
        while True:
            c = cls.buf_getch()
            if c == "Locked" and c is None:
                continue
            else:
                print()
                break

    @classmethod
    def getpass(cls, prompt='Password: ', stream=None):
        """Prompt for password with echo off"""
        # 참고 : https://www.programcreek.com/python/example/51346/msvcrt.putch
#        if sys.stdin is not sys.__stdin__:
#            return fallback_getpass(prompt, stream)
        while cls.__mutex:
            pass
        cls.__mutex = True
        index = len(cls.__buffer)
        print(prompt, end='', flush=True)
        pw = ""
        while True:
            try:
                c = cls.__buffer.pop(index)
            except Exception:
                break
            if c == '\r' or c == '\n':
                break
            if c == '\003':
                raise KeyboardInterrupt
            if c == '\b':
                pw = pw[:-1]
            else:
                pw = pw + c
        print()
        return pw


def interrupt(id, tr):
    global quit
    Buffered_ConsoleAPI.runprocess()
    getch = Buffered_ConsoleAPI.buf_getch
    while not quit:
        c = getch()
        if c == "Locked" and c is None:
            continue
        if c == 'q':
            quit = True
            log.send("Quit Command Input")
            break
        elif c == 'n':
            tr.nextsignal()
            sb.print_trafficsystem(tr.getstatus())
        elif c == 'l':
            if not log.logging:
                log.on()
            else:
                log.off()


def run(cnu_tr):
    global process
    global quit
    quit = False
    process = Process(target=interrupt, args=(1, cnu_tr))
    process.start()
    log.send("Interrupt Process started", 2)


def stop():
    global quit
    quit = True
    Buffered_ConsoleAPI.stopprocess()
    process.join()
