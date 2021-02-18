#!/usr/bin/env python3
import evdev
import ev3dev.auto as ev3
import threading
import time
from ev3dev2.sound import Sound #needed to play sound
from pyPS4Controller.controller import Controller
from pyPS4Controller.event_mapping.DefaultMapping import DefaultMapping


class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_x_press(self):
       print("Hello world")

    def on_x_release(self):
       print("Goodbye world")


class MyEventDefinition(DefaultMapping):

    def __init__(self, **kwargs):
        DefaultMapping.__init__(self, **kwargs)

    # each overloaded function, has access to:
    # - self.button_id
    # - self.button_type
    # - self.value
    # - self.overflow
    # use those variables to determine which button is being pressed
    def x_pressed(self):
        return self.button_id == 0 and self.button_type == 1 and self.value == 1

    def x_released(self):
        return self.button_id == 0 and self.button_type == 1 and self.value == 0

controller = MyController(interface="/dev/input/event4", connecting_using_ds4drv=False, event_definition=MyEventDefinition)
controller.debug = True  # you will see raw data stream for any button press, even if that button is not mapped
# you can start listening before controller is paired, as long as you pair it within the timeout window
controller.listen(timeout=60)