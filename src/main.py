# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : 4th_OOP_Project/main.py & Last Modded : 2021.05.11. ###
Coded with Python 3.9 for Windows (CRLF) by IRACK000
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os
import sys
import time
from random import *
from console.keyboard import Buffered_ConsoleAPI as cs
import console.showboard as sb
import console.keyboard as kb
import sockets.logserver as log
from classes.traffic import SUV
from classes.traffic import Truck
from classes.people import Person
from classes.traffic import TrafficLight
from classes.traffic import TrafficSystem
from classes.traffic import RealTimeTraffic


class CNU_TrafficSystem(TrafficSystem):
    def __init__(self):
        super(CNU_TrafficSystem, self).__init__(self.__cnu_traffic_make())

    def currentsignal(self):
        stat = self.getstatus()
        est = list(stat["east"].values())
        nt = list(stat["north"].values())
        if est == ["ON", "OFF", "OFF", "OFF"] and nt == ["ON", "OFF", "OFF"]:
            return 0
        elif est == ["OFF", "ON", "ON", "OFF"] and nt == ["ON", "OFF", "OFF"]:
            return 1
        elif est == ["OFF", "OFF", "ON", "ON"] and nt == ["ON", "OFF", "OFF"]:
            return 2
        elif est == ["OFF", "OFF", "ON", "OFF"] and nt == ["ON", "OFF", "OFF"]:
            return 3
        elif est == ["OFF", "OFF", "OFF", "ON"] and nt == ["ON", "OFF", "OFF"]:
            return 4
        elif est == ["ON", "OFF", "OFF", "OFF"] and nt == ["OFF", "ON", "OFF"]:
            return 5
        elif est == ["ON", "OFF", "OFF", "OFF"] and nt == ["OFF", "OFF", "ON"]:
            return 6
        else:
            return -1

    def nextsignal(self):
        cur = self.currentsignal()
        log.send("> next signal", 2)
        tl = self._dict_of_tlights
        if cur == 0:
            tl["east"].setstatus("red", False)
            tl["east"].setstatus(["green", "left"], True)
            return 1
        elif cur == 1:
            tl["east"].setstatus("green", False)
            tl["east"].setstatus("yellow", True)
            return 2
        elif cur == 2:
            tl["east"].setstatus("yellow", False)
            return 3
        elif cur == 3:
            tl["east"].setstatus("left", False)
            tl["east"].setstatus("yellow", True)
            return 4
        elif cur == 4:
            tl["east"].setstatus("yellow", False)
            tl["east"].setstatus("red", True)
            tl["north"].setstatus("red", False)
            tl["north"].setstatus("green", True)
            return 5
        elif cur == 5:
            tl["north"].setstatus("green", False)
            tl["north"].setstatus("yellow", True)
            return 6
        elif cur == 6:
            tl["north"].setstatus("yellow", False)
            tl["north"].setstatus("red", True)
            return 0
        else:
            tl["east"].setstatus("red", True)
            tl["east"].setstatus(["green", "left", "yellow"], False)
            tl["north"].setstatus("red", True)
            tl["north"].setstatus(["green", "yellow"], False)
            return 0

    def __cnu_traffic_make(self):
        return (TrafficLight("east", ("red", "green", "left", "yellow")),
                TrafficLight("north", ("red", "green", "yellow")))


class CNU_RealTimeTraffic(RealTimeTraffic):
    def moveship(self):
        if self._ship is not None:
            if self._ship.getstatus() == 0:
                self._ship.move(1)
                return
            if self._ship < self.bridge:
                if self._ship.getstatus() == 3:
                    self._ship = None
                    log.send("delete ship", 2)
                else:
                    self._ship.move(3)
                return
            if self.bridge.getstatus():
                loc = self._ship.move(self._ship.getstatus()+1)
                if loc <= 3:
                    return loc
                else:
                    self._ship = None
                    log.send("delete ship", 2)
                    self.bridge.close()
                    return -1
            else:
                if self.bridge.alert:
                    self.bridge.open()
                else:
                    self.bridge.alert = True
                return -1
        else:
            return -1

    def __find_car(self, loc_all, search):
        try:
            return loc_all.index(search)
        except Exception:
            return None

    def __shift_loc(self, loc_all, bef, aft):
        find = self.__find_car(loc_all, {'x': bef[0], 'y': bef[1]})
        to = {'x': aft[0], 'y': aft[1]}
        if find is None:
            return None
        if to not in [car.getlocation() for car in self._car]:
            self._car[find].move_in_direction(to)
            return find
        else:
            return None

    def __shift_in_dir(self, loc_all, dir, bef):
        find = self.__find_car(loc_all, {'x': bef[0], 'y': bef[1]})
        if find is None:
            return None
        if self._car[find].getdir() == dir:
            if bef[0] == -1 and dir == "east":
                to = {'x': 0, 'y': 1}
            elif bef[0] == -1 and dir == "north":
                to = {'x': 1, 'y': 0}
            elif bef[1] == -1 and dir == "east":
                to = {'x': 0, 'y': 1}
            elif bef[1] == -1 and dir == "north":
                to = {'x': 1, 'y': 0}
            if to not in [car.getlocation() for car in self._car]:
                self._car[find].move_in_direction(to)
                return find
            else:
                return None
        else:
            return "dir not matched"

    def movecar(self, light):
        loc_all = [car.getlocation() for car in self._car]
        bridge_open = self.bridge.getstatus()
        del_list = []
        # Shift Freely
        find = self.__shift_loc(loc_all, (6, 0), (0, 0))
        if find is not None:
            del_list.append(find)
        find = self.__shift_loc(loc_all, (0, 3), (0, 0))
        if find is not None:
            del_list.append(find)
        self.__shift_loc(loc_all, (5, 0), (6, 0))
        for i in range(2, 0, -1):
            self.__shift_loc(loc_all, (0, i), (0, i+1))
        # Shift affected by bridge_open
        if not bridge_open and not self.bridge.alert:
            self.__shift_loc(loc_all, (4, 0), (5, 0))
        for i in range(3, 0, -1):
            self.__shift_loc(loc_all, (i, 0), (i+1, 0))
        # Shift affected by traffic light & bridge_open
        if light in (1, 2, 3, 4) and not bridge_open:
            self.__shift_in_dir(loc_all, "east", (-1, 0))
        if light in (1, 2):
            self.__shift_in_dir(loc_all, "north", (-1, 0))
        if light in (0, 3, 4, 5, 6) and not bridge_open:
            self.__shift_in_dir(loc_all, "east", (0, -1))
        if light in (5, 6):
            self.__shift_in_dir(loc_all, "north", (0, -1))
        # Followers
        for i in range(-2, -4, -1):
            self.__shift_loc(loc_all, (i, 0), (i+1, 0))
        for i in range(-2, -6, -1):
            self.__shift_loc(loc_all, (0, i), (0, i+1))
        # Del Cars
        del_list.sort(reverse=True)
        for i in del_list:
            self.delcar(self._car[i])
        # Add a Car
        if randrange(1, 4) == 3:
            Car = choice([SUV, Truck])
            self.addcar(Car(choice(cs.OBJCLR), Person("James", "Male")))


if __name__ == '__main__':
    # Set console
    os.system("MODE CON cols=100 lines=40")
    os.system("TITLE OOP Project Main")
    if len(sys.argv) >= 2 and sys.argv[1] == 'LOG_ON':
        log.on(show=True)
    log.setlevel(2)
    print("Windows에서 동작이 보장됩니다. macOS에서는 테스트되지 않았습니다.")
    if input("Do you want to run in Unicode mode? (no : n) : ") == 'n':
        cs.setcodepage(unicode=False)
    cs.hidecurs(True)

    # Init
    tr = CNU_TrafficSystem()
    rt = CNU_RealTimeTraffic()
    kb.run(tr)

    # Set Speed: Time Generalization
    times = []
    for j in range(5):
        start = time.time()
        for i in range(5000000):
            pass
        times.append(time.time() - start)
    times.sort()
    per = times[len(times) // 2] #= sum(times)/len(times)
    log.send(per)
    SET_SPEED = int(5000000 / per * 0.5)
    log.send("speed set to " + str(SET_SPEED))

    # Run Once
    sb.print_struct()
    tr.nextsignal()
    sb.print_trafficsystem(tr.getstatus())
    sb.print_bridge(rt.bridge.getstatus())

    # Loop
    speed: int = 0
    repeat: int = 0
    while not kb.quit:
        speed = (speed + 1) % SET_SPEED
        if speed == 0:
            repeat = (repeat + 1) % 3
            if repeat == 2:
                tr.nextsignal()
                sb.print_trafficsystem(tr.getstatus())
            sb.print_bridge(rt.bridge.getstatus())
            sb.print_ship(rt.getshipstatus())
            rt.movecar(tr.currentsignal())
            sb.print_cars(rt.gettuple())
            if rt.isthereaship():
                rt.moveship()
            sb.print_ship(rt.getshipstatus())

    # Log Off
    kb.stop()
    log.send("Log OFF")
    cs.gotoxy(2, 36)
    cs.pause()
    log.off()
