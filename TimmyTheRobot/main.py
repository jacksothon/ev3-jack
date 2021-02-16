#!/usr/bin/env python3
"""
When the PS4 is paried with the device it creates three event files.

/dev/input/event2 (touchpad events)
/dev/input/event3 (controller movement, like tilting, shaking, etc...)
/dev/input/event4 (buttons, sticks, etc...)
Each event provides five values, but we only need the event ID, code, and value. Here is a list of all events I could map:
"""
## Import libraries ##
import evdev
import ev3dev.auto as ev3
import threading
import time
from ev3dev2.sound import Sound #needed to play sound

#some music 
spkr = Sound()
#spkr.play_file('bark.wav')
spkr.speak('yooo')


## Converting Ps4 events into understandable code 
def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def scale(val, src, dst):
    return (float(val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]

def scale_stick(value):
    return scale(value,(0,255),(-500,500))

def dc_clamp(value):
    return clamp(value,-500,500)

## Initializing ##
print("Finding ps4 controller...")
devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
ps4dev = devices[0].fn

gamepad = evdev.InputDevice(ps4dev)

forward_speed = 0
side_speed = 0
grab_speed = 0
running = True

## The Motors ##
class MotorThread(threading.Thread):
    def __init__(self):
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.claw_motor = ev3.MediumMotor(ev3.OUTPUT_D)
        threading.Thread.__init__(self)

    def run(self):
        print("Engine running! Jack")
        while running:
            self.right_motor.run_forever(speed_sp=dc_clamp(forward_speed+side_speed))
            self.left_motor.run_forever(speed_sp=dc_clamp(-forward_speed+side_speed))
            self.claw_motor.run_forever(speed_sp=dc_clamp(grab_speed))
        self.right_motor.stop()
        self.left_motor.stop()
        self.claw_motor.stop()

motor_thread = MotorThread()
motor_thread.setDaemon(True)
motor_thread.start()

## The PS4 Controller Mapping ##

for event in gamepad.read_loop():   #this loops infinitely
    # map the controller left analog stick to the two driving motors
    if event.type == 3:             #left stick is moved
        if event.code == 0:         #X axis on left stick
            forward_speed = -scale_stick(event.value)
        if event.code == 1:         #Y axis on left stick
            side_speed = scale_stick(event.value)
        if side_speed < 100 and side_speed > -100:
            side_speed = 0
        if forward_speed < 100 and forward_speed > -100:
            forward_speed = 0

    # map the controller right analog stick to the grab claw/LargeMotor
    if event.type == 3:
        if event.code == 2:
            grab_speed = scale_stick(event.value)
        if grab_speed < 100 and -grab_speed > -100:
            grab_speed = 0
    if event.type == 3:
        if event.code == 4:
            grab_speed = -scale_stick(event.value)
        if grab_speed < 100 and grab_speed > -100:
            grab_speed = 0

    # button X exits the Program
    if event.type == 1 and event.code == 305 and event.value == 1:
        print("X button is pressed. Stopping.")
        running = False
        time.sleep(0.5) # Wait for the motor thread to finish
        break