#!/usr/bin/env python3
from pyPS4Controller.controller import Controller
import evdev
import ev3dev.auto as ev3
import threading
import time
from ev3dev2.sound import Sound #needed to play sound


class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)


controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen()