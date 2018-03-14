import RPi.GPIO as rg

rg.setmode(rg.BCM)

class DTPin:
    def __init__(self, pin=16):
        self.dt = rg.setup(pin, rg.IN)
    def value(self):
        return rg.input(self.dt)

class SCKPin:
    def __init__(self, pin=20):
        self.sck = rg.setup(pin, rg.OUT)
    def on(self):
        rg.output(self.sck, 1)
    def off(self):
        rg.output(self.sck, 0)
    def pulse(self):
        rg.output(self.sck, 1)
        rg.output(self.sck, 0)
    def value(self):
        return rg.input(self.sck)
