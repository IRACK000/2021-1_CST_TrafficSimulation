# -*- coding: utf-8 -*-
import os
import sys
from random import *
import unittest

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from src.console.keyboard import Buffered_ConsoleAPI as cs
import src.console.showboard as sb
from src.classes.traffic import SUV
from src.classes.traffic import Truck
from src.main import CNU_TrafficSystem
from src.main import CNU_RealTimeTraffic
from src.classes.bridge import *


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
        sb.print_struct()
        tr.nextsignal()
        sb.print_trafficsystem(tr.getstatus())

    def tearDown(self):
        """테스트 종료 후 실행"""
        cs.clear()
        cs.printcs("Unit Test: '%s' Finished." % os.path.basename(__file__))

    def test_runs(self):
        """단순 실행여부 판별하는 테스트 메소드"""
        sb.print_struct()
        tr.nextsignal()
        sb.print_trafficsystem(tr.getstatus())

    def test_height_compare(self):
        mship = MerchantShip(0)
        fship = FishingBoat(0)
        bridge = Bridge()
        self.assertEqual(mship < bridge, mship._height < bridge._height)
        self.assertEqual(fship > bridge, fship._height > bridge._height)
        self.assertEqual(fship <= mship, fship._height <= mship._height)
        self.assertEqual(fship >= mship, fship._height >= mship._height)
        self.assertEqual(fship == mship, fship._height == mship._height)

    def test_bridge_not_open_when_there_is_a_fishingboat(self):
        rt._ship = FishingBoat(0)
        for i in range(4):
            if rt.isthereaship():
                rt.moveship()
        self.assertFalse(rt.bridge.getstatus())

    def test_bridge_open_when_there_is_a_merchantship(self):
        rt._ship = MerchantShip(0)
        for i in range(5):
            if rt.isthereaship():
                rt.moveship()
        self.assertTrue(rt.bridge.getstatus())

    def test_bridge_close(self):
        rt._ship = MerchantShip(0)
        for i in range(6):
            if rt.isthereaship():
                rt.moveship()
        self.assertFalse(rt.bridge.getstatus())

    def test_bridge_not_open_when_there_is_a_car_on_bridge(self):
        rt._ship = MerchantShip(0)
        Car = choice([SUV, Truck])
        rt._car[rt.addcar(Car(0, []))].move_in_direction({'x': 5, 'y': 0})
        if rt.isthereaship():
            rt.moveship()
        self.assertFalse(rt.bridge.getstatus())
        self.assertFalse(rt.bridge.alert)
        for i in range(4):
            if rt.isthereaship():
                rt.moveship()
        self.assertTrue(rt.bridge.getstatus())
        self.assertTrue(rt.bridge.alert)
        if rt.isthereaship():
            rt.moveship()
        self.assertFalse(rt.bridge.getstatus())
        self.assertFalse(rt.bridge.alert)


if __name__ == '__main__':
    unittest.main()
