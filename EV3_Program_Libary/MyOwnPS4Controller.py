from pyPS4Controller.controller import Controller


class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_x_press(self):
       print("Hello world")

    def on_x_release(self):
       print("Goodbye world")
    
    def on_L1_press(self):
        print('pressed l1')


controller1 = MyController()
controller1.on_L1_press(