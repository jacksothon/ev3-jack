import evdev
import ev3dev.auto as ev3
import threading
import time
from ev3dev2.sound import Sound #needed to play sound


#Initialising (the ps4 connection code was obtained from evdev documentation)
#This allows me to take input from multiple event files, as seen below when i use -------
print("looking for ps4 controller") 
devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
ps4dev = devices[0].fn

controller = evdev.InputDevice(ps4dev)

## Used to convert Ps4 byte data from events file
def clamp(n, minn, maxn):
    return max(min(maxn, n), minn) #creating a clamp function which restricts a value to set values

def scale(val, src, dst):
    return (float(val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]
    # a scale funtion which converts the analogue stick values into values easier to work with
    # for the analogue stick it goes from 0 --> 255

def scale_stick(value):
    return scale(value,(0,255),(-1000,1000)) 
    # you can see here that it scales the values to -1000 and 1000 which ev3motors understand

def dc_clamp(value):
    return clamp(value,-1000,1000) #using clamp to restrict to -1000 and 1000 which is max speed on lego motors


forward_speed = 0
side_speed = 0
grab_speed = 0
running = True

# all the motors #
class motorthread(threading.Thread):
    def __init__(self):
        self.rightmotor = ev3.Largemotor(ev3.OUTPUT_C)
        self.leftmotor = ev3.Largemotor(ev3.OUTPUT_B)
        self.clawmotor = ev3.Largemotor(ev3.OUTPUT_D)
        threading.Thread.__init__(self)

    def run(self):
        while running: #this will run forever 
            self.rightmotor.run_forever(speed_sp=dc_clamp(forward_speed+side_speed))
            self.leftmotor.run_forever(speed_sp=dc_clamp(-forward_speed+side_speed))
            self.clawmotor.run_forever(speed_sp=dc_clamp(grab_speed))
        self.rightmotor.stop()
        self.leftmotor.stop()
        self.clawmotor.stop()

motor_thread = motorthread() #assigning the object/class???
motor_thread.setDaemon(True) #something to allow it to run all at the same time
motor_thread.start() #execute the class 

# mapping controller events to change the speed variables.

for event in controller.read_loop(): #this will loop infinitely through all the events
    if event.type == 1: # mapping the R2 button to move robot forward
        if event.code == 311:
            forward_speed = scale_stick(event.value) #if R2 pressed forward speed is increased depending on how much you press R2
            
    if event.type == 1 and event.code == 305 and event.value == 1:
        print("X button is pressed. Stopping.")
        running = False
        time.sleep(0.5) # Wait for the motor thread to finish
        break













"""
/dev/input/event3 (controller movement, like tilting, shaking, etc...)
/dev/input/event4 (buttons, sticks, etc...)
Each event provides five values, but we only need the event ID, 
code, and value. Here is a list of all events I could map:
"""