#!/usr/bin/env python3
from ev3dev.ev3 import *
import os
import controller

mL = LargeMotor('outB'); 
mR = LargeMotor('outC'); 
crane = MediumMotor('outD'); 
os.system('setfont Lat15-TerminusBold14')


mL.run_timed(time_sp = 600, speed_sp = 900)
mR.run_timed(time_sp = 600, speed_sp = 900)

crane.run_to_rel_pos(position_sp=-300, speed_sp = 200)

"""
class MyController(controller):

    def __init__(self, **kwargs):
        controller.__init__(self, **kwargs)

    def on_x_press(self):
       crane.run_to_rel_pos(position_sp=-300, speed_sp = 200)

    def on_x_release(self):
       print("Goodbye world")

controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen()




"""