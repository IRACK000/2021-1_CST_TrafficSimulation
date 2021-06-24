# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : 4th_OOP_Project/class/people.py & Last Modded : 2021.05.05. ###
Coded with Python 3.9 for Windows (CRLF)
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os
import sys
import abc

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import sockets.logserver as log


class Person(object):
    """Person class"""

    def __init__(self, name, gender):
        self.name = name
        self.gender = gender

    def eat(self, food):
        log.send(self.name + " eats " + food.name)
        del food


class People(Person):
    """People class"""

    def __init__(self, max_people):
        self.__max_people = max_people
        self.__list = []

    def gettuple(self):
        return tuple(self.___list)

    def addperson(self, person):
        if len(self.___list) < self.__max_people:
            self.___list.append(person)
        else:
            return -1

    def delperson(self, person):
        if person in self.___list:
            self.___list.remove(person)
        else:
            return -1

    @classmethod
    def makegroup(cls, group=None, prsn={}):
        """input = {name: gender}"""
        if group is None:
            group = People(len(prsn))
        for name, gender in prsn.items():
            group.addperson(Person(name, gender))
        return group


class Food(object):
    """Food class"""

    def __init__(self, name):
        self.name = name


class Foods(object):
    """Foods class"""

    def __init__(self, max_food):
        self.__max_food = max_food
        self.__list = []

    def gettuple(self):
        return tuple(self.___list)

    def addfood(self, food):
        if len(self.___list) < self.__max_food:
            self.___list.append(food)
        else:
            return -1

    def delfood(self, food):
        if food in self.___list:
            self.___list.remove(food)
        else:
            return -1

    @classmethod
    def maketrunk(cls, trunk=None, foods=()):
        if trunk is None:
            trunk = Foods(len(foods))
        for food in foods:
            trunk.addfood(Foods(food))
        return trunk
