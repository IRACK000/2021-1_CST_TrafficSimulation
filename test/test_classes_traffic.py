# -*- coding: utf-8 -*-
import os
import sys
import unittest
from random import *

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from src.console.keyboard import Buffered_ConsoleAPI as cs
import src.console.showboard as sb
from src.classes.traffic import *
from src.classes.bridge import MerchantShip
from src.main import CNU_TrafficSystem
from src.main import CNU_RealTimeTraffic


class CustomTests(unittest.TestCase):
    def setUp(self):
        """테스트 시작되기 전 실행"""
        os.system("MODE CON cols=150 lines=40")
        os.system("TITLE OOP Project Main")
        cs.hidecurs(True)
        cs.clear()

        # Init
        global tr
        global rt
        tr = CNU_TrafficSystem()
        rt = CNU_RealTimeTraffic()

    def tearDown(self):
        """테스트 종료 후 실행"""
        cs.clear()
        cs.printcs("Unit Test: '%s' Finished." % os.path.basename(__file__))

    def test_runs(self):
        """단순 실행여부 판별하는 테스트 메소드"""
        sb.print_struct()
        tr.nextsignal()
        sb.print_trafficsystem(tr.getstatus())

    def test_led_on_and_off(self):
        led = LEDLamp("red")
        led.on()
        self.assertEqual(led.getstatus()[1], "ON")
        print(led)
        led.off()
        self.assertEqual(led.getstatus()[1], "OFF")
        print(led)

    def test_trafficlight_operation(self):
        light = TrafficLight("north", ("red", "green", "yellow"))
        print(light)
        self.assertEqual(len(light), 3)
        light.addled("left")
        self.assertNotEqual(len(light), 4)
        self.assertEqual(light.delled("sldkfjeel"), -1)
        light.delled("yellow")
        light.addled("left")
        self.assertEqual(len(light), 3)
        self.assertEqual(light.setstatus("sdfesfs", True), -1)
        light.setstatus(["red", "green", "left"], True)
        stat = light.getstatus()
        self.assertEqual(list(stat.keys()), ["red", "green", "left"])
        self.assertEqual(list(stat.values()), ["ON", "ON", "ON"])
        light.setstatus(["red", "green", "left"], False)
        stat = light.getstatus()
        self.assertEqual(list(stat.keys()), ["red", "green", "left"])
        self.assertEqual(list(stat.values()), ["OFF", "OFF", "OFF"])

    def test_add_car(self):
        Car = choice([SUV, Truck])
        index = rt.addcar(Car(0, []))
        self.assertNotEqual(index, -1)
        Car = choice([SUV, Truck])
        index = rt.addcar(Car(0, []))
        self.assertNotEqual(index, -1)

    def test_add_car_fail_when_there_is_car_already_in_locations(self):
        self.test_add_car()
        Car = choice([SUV, Truck])
        index = rt.addcar(Car(0, []))
        self.assertEqual(index, -1)

    def test_do_not_move_car_when_bridge_alert_is_true(self):
        rt._ship = MerchantShip(0)
        Car = choice([SUV, Truck])
        index = rt.addcar(Car(0, []))
        rt._car[index].move_in_direction({'x': 4, 'y': 0})
        for i in range(5):
            if rt.isthereaship():
                rt.moveship()
        self.assertTrue(rt.bridge.getstatus())
        self.assertTrue(rt.bridge.alert)
        rt.movecar(tr.currentsignal())
        self.assertNotEqual(list(rt._car[index].getlocation().values()), [5, 0])
        if rt.isthereaship():
            rt.moveship()
        self.assertFalse(rt.bridge.getstatus())
        self.assertFalse(rt.bridge.alert)
        rt.movecar(tr.currentsignal())
        self.assertEqual(list(rt._car[index].getlocation().values()), [5, 0])

    def test_is_there_any_cars_that_locate_in_same_xy(self, test_repeat=50):
        for i in range(test_repeat):
            if i % 3 == 2:
                tr.nextsignal()
                sb.print_trafficsystem(tr.getstatus())
            sb.print_bridge(rt.bridge.getstatus())
            sb.print_ship(rt.getshipstatus())
            rt.movecar(tr.currentsignal())
            sb.print_cars(rt.gettuple())
            if rt.isthereaship():
                rt.moveship()
            sb.print_ship(rt.getshipstatus())
            loc_all = [car.getlocation() for car in rt._car]
            for car in loc_all:
                for comp in loc_all:
                    if comp is not car:
                        self.assertNotEqual(comp, car)


if __name__ == '__main__':
    unittest.main()
