import RPi.GPIO as rg

# Mode of True tells the Raspberry Pi to set the pin mode
# to BOARD MODE while a Mode of False set's it to BCM MODE
def hx711_init(mode):
    if mode:
        rg.setmode(rg.BOARD)
    else:
        rg.setmode(rg.BCM)

class DTPin:
    def __init__(self, pin):
        self.dt = pin
        rg.setup(pin, rg.IN)
    def value(self):
        return rg.input(self.dt)

class SCKPin:
    def __init__(self, pin):
        self.sck = pin
        rg.setup(pin, rg.OUT)
    def on(self):
        rg.output(self.sck, 1)
    def off(self):
        rg.output(self.sck, 0)
    def pulse(self):
        rg.output(self.sck, 1)
        rg.output(self.sck, 0)
    def value(self):
        return rg.input(self.sck)
