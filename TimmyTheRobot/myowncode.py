import asyncio
from evdev import InputDevice, categorize, ecodes

event4 = InputDevice('/dev/input/event4')
# to keep it simple I will just do event4, so just sticking to buttons. 

#Initialising (the ps4 connection code was obtained from evdev documentation)
print("looking for ps4 controller") 
devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
ps4dev = devices[0].fn

gamepad = evdev.InputDevice(ps4dev)

forward_speed = 0
side_speed = 0
grab_speed = 0
running = True



"""
/dev/input/event3 (controller movement, like tilting, shaking, etc...)
/dev/input/event4 (buttons, sticks, etc...)
Each event provides five values, but we only need the event ID, 
code, and value. Here is a list of all events I could map:
"""