# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : 4th_OOP_Project/class/traffic.py & Last Modded : 2021.05.05. ###
Coded with Python 3.9 for Windows (CRLF) by IRACK000
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os
import sys
import abc
from random import *

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from console.util import ConsoleAPI as cs
import sockets.logserver as log
import classes.people as pple
from classes.bridge import MerchantShip
from classes.bridge import FishingBoat
from classes.bridge import Bridge


class LEDLamp(object):
    """LEDLamp class"""

    def __init__(self, color):
        super(LEDLamp, self).__init__()
        self.__color: str = color
        self.__light: bool = False
        log.send("New LEDLamp Created", 3)

    def __str__(self):
        return self.__color + " lamp" + "(ON)" if self.__light else "(OFF)"

    def on(self):
        """lamp turn on"""
        self.__light: bool = True
        log.send("LEDLamp Tun On", 3)

    def off(self):
        """lamp turn off"""
        self.__light: bool = False
        log.send("LEDLamp Tun Off", 3)

    def getstatus(self):
        """return lamp status"""
        return self.__color, "ON" if self.__light else "OFF"


class TrafficLight(object):
    """TrafficLight class"""

    def __init__(self, name, ledlist):
        super(TrafficLight, self).__init__()
        self.name: str = name
        self.__max_led: int = len(ledlist)  # LED 개수는 최소 생성시 고정.
        self.__light: dict = {}
        log.send("New TrafficLight %s(%d)" % (self.name, self.__max_led), 2)
        for clr in ledlist:
            self.addled(clr)

    def __len__(self):
        return len(self.__light)

    def __str__(self):
        s = ""
        for led in self.__light.values():
            s += "%s: %s " % led.getstatus()
        return s

    def addled(self, clr):
        """add a led lamp to TrafficLight"""
        if len(self.__light) < self.__max_led:
            self.__light[clr] = LEDLamp(clr)
            log.send("%s LEDLamp added" % clr, 3)
        else:
            print("ERROR: Too many lamps")
            return -1

    def delled(self, key):
        """del a led lamp from TrafficLight"""
        try:
            del self.__light[key]
            log.send("%s LEDLamp deleted" % key, 3)
        except Exception as e:
            print(e)
            return -1

    def setstatus(self, key, on):
        """set led status"""
        if type(key) == list or type(key) == tuple:
            for i in key:
                self.setstatus(i, on)
        else:
            try:
                if on:
                    self.__light[key].on()
                else:
                    self.__light[key].off()
            except Exception as e:
                print(e)
                return -1

    def getstatus(self):
        stat = {}
        for key, val in self.__light.items():
            stat[key] = val.getstatus()[1]
        return stat


class TrafficSystem(metaclass=abc.ABCMeta):
    """TrafficSystem class"""

    def __init__(self, objs):
        super(TrafficSystem, self).__init__()
        self._dict_of_tlights = {}
        log.send("New TrafficSystem Created", 2)
        for obj in objs:
            self.addlight(obj)

    def __len__(self):
        return len(self._dict_of_tlights)

    def addlight(self, obj):
        self._dict_of_tlights[obj.name] = obj
        log.send("%s TrafficLight added" % obj.name, 3)

    def dellight(self, key):
        try:
            del self._dict_of_tlights[key]
            log.send("%s TrafficLight deleted" % key, 3)
        except Exception as e:
            print(e)
            return -1

    def getstatus(self):
        stat = {}
        for key, val in self._dict_of_tlights.items():
            stat[key] = val.getstatus()
        return stat

    @abc.abstractmethod
    def nextsignal(self):
        pass


class Frame(object):
    """Frame class"""

    def __init__(self, color):
        self.__color: str = color

    def getcolor(self):
        return self.__color

    def changecolor(self, color):
        self.__color: str = color


class Engine(object):
    """Engine class"""

    def __init__(self):
        self.__status: bool = False

    def getstatus(self):
        return self.__status

    def setstatus(self, on):
        self.__status: bool = on


class Wheel(object):
    """Wheel class"""

    def __init__(self):
        self.__move: bool = False

    def getstatus(self):
        return self.__move

    def setstatus(self, move):
        self.__move: bool = move


class Car(metaclass=abc.ABCMeta):
    """Abstract Car class"""

    def __init__(self, color, driver, maxpsgr, maxfood):
        self.frame = Frame(color)
        self.changedriver(driver)
        self._lf_whl = Wheel()
        self._rf_whl = Wheel()
        self._lb_whl = Wheel()
        self._rf_whl = Wheel()
        self._engine = Engine()
        self.whl = (self._lf_whl, self._rf_whl, self._lb_whl, self._rf_whl)
        self.__direction = choice(["east", "north"])
        self.__max_passenger: int = maxpsgr
        self.__max_food: int = maxfood
        self.passenger = pple.People(self.__max_passenger)
        self.trunk = pple.Foods(self.__max_food)
        self._location = 0

    def getdir(self):
        return self.__direction

    def getlocation(self):
        return self._location

    def changedriver(self, driver):
        self.driver = driver

    def __set_wheel(self, stat):
        for whl in self.whl:
            whl.setstatus(stat)

    def move_in_direction(self, location):
        self.move()
        self._location = location
        self.stop()

    def move(self):
        self._engine.setstatus(True)
        self.__set_wheel(True)

    def stop(self):
        self._engine.setstatus(False)
        self.__set_wheel(False)


class SUV(Car):
    """SUV class"""

    def __init__(self, color, driver):
        super().__init__(color, driver, 3, 2)


class Truck(Car):
    """Truck class"""

    def __init__(self, color, driver):
        super().__init__(color, driver, 1, 4)


class RealTimeTraffic(metaclass=abc.ABCMeta):
    """RealTimeTraffic class"""

    def __init__(self):
        self.__max_car = 17
        self._car = []
        self.bridge = Bridge()
        self._ship = None

    def __len__(self):
        return len(self._car)

    def gettuple(self):
        return tuple(self._car)

    def addcar(self, car):
        if len(self._car) < self.__max_car:
            loc_all = [car.getlocation() for car in self._car]
            to = [{'x': 0, 'y': -5}, {'x': -3, 'y': 0}]
            for i in (1, 2):
                select = choice(to)
                to.remove(select)
                if select in loc_all:
                    continue
                else:
                    self._car.append(car)
                    index = len(self._car) - 1
                    self._car[index].move_in_direction(select)
                    log.send("create a car", 2)
                    return index
            return -1
        else:
            return -1

    def delcar(self, car):
        if car in self._car:
            self._car.remove(car)
            log.send("delete a car", 2)
        else:
            return -1

    def __gen_ship(self):
        res = randrange(1, 6)
        if res == 1:
            self._ship = MerchantShip(choice(cs.OBJCLR))
            log.send("create merchantchip", 2)
            return True
        elif res == 2:
            self._ship = FishingBoat(choice(cs.OBJCLR))
            log.send("create fishingboat", 2)
            return True
        else:
            return False

    def isthereaship(self):
        if self._ship is None:
            return self.__gen_ship()
        else:
            return True

    def getshipstatus(self):
        if self._ship is not None:
            return self._ship.getstatus(), self._ship.getcolor()
        else:
            return -1

    @abc.abstractmethod
    def moveship(self):
        pass

    @abc.abstractmethod
    def movecar(self):
        pass
