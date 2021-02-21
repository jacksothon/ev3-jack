#!/usr/bin/env python3
import evdev
import ev3dev.auto as ev3
import threading
import time
from ev3dev2.sound import Sound #needed to play sound


## Used to convert Ps4 byte data from events file
def clamp(n, minn, maxn):
    return max(min(maxn, n), minn) #creating a clamp function which restricts a value to set values

def scale(val, src, dst):
    return (float(val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]
    # a scale funtion which converts the analogue stick values into values easier to work with
    # for the analogue stick it goes from 0 --> 255

def scale_stick(value):
    return scale(value,(0,255),(-1000,1000)) 

def scale_stick_lift(value): #same as scale_stick but the R2 and R1 only go from 0-255 while analoge sticks go from -255 --> 255
    return scale(value,(0,255),(0,1000)) 

    # you can see here that it scales the values to -1000 and 1000 which ev3motors understand
""""
def (value):
    return clamp(value,-1000,1000) #using clamp to restrict to -1000 and 1000 which is max speed on lego motors
"""

#Initialising (the ps4 connection code was obtained from evdev documentation)
#This allows me to take input from multiple event files, as seen below
print("looking for ps4 controller") 
devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
ps4dev = devices[0].fn

controller = evdev.InputDevice(ps4dev)


forward_speed_L = 0
forward_speed_R = 0
side_speed_L = 0 # variable used to alter forward speed to allow a change in direction.
side_speed_R = 0 
grab_speed = 0
running = True


# all the motors #
class MotorThread(threading.Thread):
    def __init__(self):
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.claw_motor = ev3.MediumMotor(ev3.OUTPUT_D)
        threading.Thread.__init__(self)

    def run(self):
        print('the engine is running!')
        while running: #this will run forever 
            self.right_motor.run_forever(speed_sp=(forward_speed_R + side_speed_R ))
            self.left_motor.run_forever(speed_sp=(forward_speed_L + side_speed_L ))
            self.claw_motor.run_forever(speed_sp=(grab_speed))
        self.right_motor.stop()
        self.left_motor.stop()
        self.claw_motor.stop()

motor_thread = MotorThread() 
motor_thread.setDaemon(True)
motor_thread.start() #execute


# mapping controller events to change the speed variables.
for event in controller.read_loop(): #this will loop infinitely through all the events
    if event.type == 3: #moving back and forwards with Y axis of left stick
        if event.code == 1: # y axis of left joystick
            forward_speed_L = scale_stick(event.value)
            forward_speed_R = scale_stick(event.value)
        
        if event.code == 3: # x axis of right joystick // if we move joystick to right: 
            side_speed_R = -1*(scale_stick(event.value))
            side_speed_L = scale_stick(event.value)

        if event.code == 2:
            grab_speed = (scale_stick_lift(event.value))
        if event.code == 5:
            grab_speed = -1*(scale_stick_lift(event.value))

            
    if event.type == 1 and event.code == 304 and event.value == 1:
            print("EMERGENCY SHUTDOWN \nPlutonium-238: somehow gone \nENGINE: bro ")
            time.sleep(2) # time to read shutdown message
            running = False
            time.sleep(0.5) # Wait for the motor thread to finish
            break




