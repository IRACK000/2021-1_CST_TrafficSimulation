# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : 4th_OOP_Project/class/bridge.py & Last Modded : 2021.05.10. ###
Coded with Python 3.9 for Windows (CRLF)
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os
import sys
import abc

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import sockets.logserver as log


class Engine(object):
    def __init__(self):
        self.__move: bool = False

    def on(self):
        self.__move = True

    def off(self):
        self.__move = False

    def getstatus(self):
        return self.__move


class Ship(metaclass=abc.ABCMeta):
    def __init__(self, color, height):
        self.__color: str = color
        self._height: int = height
        self.__location = 0

    def __lt__(self, other):
        return self._height < other._height

    def __gt__(self, other):
        return self._height > other._height

    def __le__(self, other):
        return self._height <= other._height

    def __ge__(self, other):
        return self._height >= other._height

    def __eq__(self, other):
        return self._height == other._height

    def __ne__(self, other):
        return self._height != other._height

    def getcolor(self):
        return self.__color

    def setcolor(self, color):
        self.__color: str = color

    def move(self, location):
        self.__location = location
        return self.__location

    def getstatus(self):
        return self.__location


class MerchantShip(Ship):
    def __init__(self, color):
        super(MerchantShip, self).__init__(color, 20)
        self.__stock = []

    def loadstock(self, obj):
        self.__stock.append(obj)

    def unloadstock(self, index):
        self.__stock.pop(index)

    def getstock(self):
        return tuple(self.__stock)


class FishingBoat(Ship):
    def __init__(self, color):
        super(FishingBoat, self).__init__(color, 4)
        self.__fishes = []

    def addfish(self, obj):
        self.__fishes.append(obj)

    def discardfish(self, index):
        self.__fishes.pop(index)

    def getfishtuples(self):
        return tuple(self.__fishes)


class Bridge(object):
    def __init__(self):
        self._height: int = 8
        self.__open: bool = False
        self.alert: bool = False

    def __lt__(self, other):
        return self._height < other._height

    def __gt__(self, other):
        return self._height > other._height

    def __le__(self, other):
        return self._height <= other._height

    def __ge__(self, other):
        return self._height >= other._height

    def __eq__(self, other):
        return self._height == other._height

    def __ne__(self, other):
        return self._height != other._height

    def open(self):
        self.alert = True
        self.__open = True
        log.send(">> bridge open", 2)

    def close(self):
        self.alert = False
        self.__open = False
        log.send(">> bridge close", 2)

    def getstatus(self):
        return self.__open
