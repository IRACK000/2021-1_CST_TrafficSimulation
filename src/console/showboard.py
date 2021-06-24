# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : console.showboard & Last Modded : 2021.05.05. ###
Coded with Python 3.9 for Windows (CRLF) by IRACK000
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os
import sys

sys.path.append(os.path.dirname(__file__))
from util import ConsoleAPI as cs


def print_struct():
    cs.clear()
    cs.printcs("                  ■    ■\n" * 9
             + "■■■■■■■■■■    ■■■■■■■■■■■■■■■■■■■■■■■■■■■\n\n\n"
             + "■■■■■■■■■■    ■■■■■■■■■■■■■■■■■■■■■■■■■■■\n"
             + "                  ■    ■\n" * 15
             + "\n\n\n\n\n [q: quit] [l: log on/off] [n: next sign]", cs.BRIGHT_WHITE)


def print_bridge(open=False):
    if open:
        cs.printcs("■          ■", 51, 7, cs.BRIGHT_GREEN)
        cs.printcs("■          ■", 51, 8, cs.BRIGHT_GREEN)
        cs.printcs("■          ■", 51, 9, cs.BRIGHT_GREEN)
        cs.printcs("■          ■", 51, 10, cs.BRIGHT_GREEN)
        cs.printcs("■          ■", 51, 11, cs.BRIGHT_GREEN)
        cs.printcs("■          ■", 51, 12, cs.BRIGHT_GREEN)
        cs.printcs("              ", 51, 13)
    else:
        cs.printcs("              ", 51, 7)
        cs.printcs("              ", 51, 8)
        cs.printcs("■          ■", 51, 9)
        cs.printcs("■■■■■■■", 51, 10, cs.BRIGHT_WHITE)
        cs.printcs("              ", 51, 11, cs.BRIGHT_WHITE)
        cs.printcs("              ", 51, 12, cs.BRIGHT_WHITE)
        cs.printcs("■■■■■■■", 51, 13, cs.BRIGHT_WHITE)


def print_trafficsystem(stat):
    for key, val in stat.items():
        if key == "east":
            cs.printcs("●", 15, 14, cs.RED if val["red"] == "ON" else cs.GREY)
            cs.printcs("●", 15, 15, cs.GREEN if val["green"] == "ON" else cs.GREY)
            cs.printcs("←", 15, 16, cs.GREEN if val["left"] == "ON" else cs.GREY)
            cs.printcs("●", 15, 17, cs.YELLOW if val["yellow"] == "ON" else cs.GREY)
        elif key == "north":
            cs.printcs("●", 27, 15, cs.RED if val["red"] == "ON" else cs.GREY)
            cs.printcs("●", 29, 15, cs.GREEN if val["green"] == "ON" else cs.GREY)
            cs.printcs("●", 31, 15, cs.YELLOW if val["yellow"] == "ON" else cs.GREY)


def print_cars(cars, before=[[], []]):
    for i in before[0]:
        cs.printcs("      ", i, 11)
        cs.printcs("      ", i, 12)
    before[0].clear()
    for i in before[1]:
        cs.printcs("    ", 21, i)
    before[1].clear()
    all_loc = [car.getlocation() for car in cars]
    all_clr = [car.frame.getcolor() for car in cars]
    for loc, clr in zip(all_loc, all_clr):
        if loc['y'] == 0:
            if loc['x'] == 6:
                x = 67
            elif loc['x'] == 5:
                x = 55
            elif loc['x'] > 0:
                x = (loc['x']+3) * 6 + 1
            else:
                x = (loc['x']+3) * 6 + 3
            cs.printcs("■■", x, 11, clr)
            cs.printcs("■", x+4, 11, cs.BLUE if clr != cs.BLUE else cs.BRIGHT_RED)
            cs.printcs("■■■", x, 12, clr)
            before[0].append(x)
        else:
            if loc['y'] > 0:
                y = loc['y']*-3 + 11
            else:
                y = loc['y']*-3 + 10
            cs.printcs("■", 21, y, cs.BLUE if clr != cs.BLUE else cs.BRIGHT_RED)
            cs.printcs("■", 23, y, clr)
            cs.printcs("■■", 21, y+1, clr)
            cs.printcs("■■", 21, y+2, clr)
            before[1].extend((y, y+1, y+2))


def print_ship(ship, before=[-1]):
    if before[0] != -1:
        for i in range(1, 8):
            cs.printcs("        ", 55, before[0]*-6+20+i)
    if ship != -1:
        before[0] = ship[0]
        cs.printcs("  ■  ", 55, ship[0]*-6+21, ship[1])
        cs.printcs("■■■", 55, ship[0]*-6+22, ship[1])
        cs.printcs("■■■", 55, ship[0]*-6+23, ship[1])
        cs.printcs("■■■", 55, ship[0]*-6+24, ship[1])
        cs.printcs("■■■", 55, ship[0]*-6+25, ship[1])
        cs.printcs("  ■  ", 55, ship[0]*-6+26, ship[1])


if __name__ == '__main__':
    os.system("MODE CON cols=150 lines=40")
    if input("Do you want to run in Unicode mode? (yes : y) : ") != 'y':
        cs.setcodepage(unicode=False)
    print_struct()
    cs.gotoxy(1, 1)
    cs.pause("")
    print_bridge(True)
    cs.gotoxy(1, 1)
    cs.pause("")
    print_bridge(False)

    cs.pause()
