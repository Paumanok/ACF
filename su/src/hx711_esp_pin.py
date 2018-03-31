from machine import Pin, freq

# Increase esp clock frequency for the SCK signal to operate
# fast enough to prevent data saturation
freq(160000000)

class DTPin:
    def __init__(self, pin=4):
        self.dt = Pin(pin, Pin.IN)
    def value(self):
        return self.dt.value()

class SCKPin:
    def __init__(self, pin=5):
        self.sck = Pin(pin, Pin.OUT)
    def on(self):
        self.sck.value(1)
    def off(self):
        self.sck.value(0)
    def pulse(self):
        self.sck.value(1)
        self.sck.value(0)
    def value(self):
        return self.sck.value()
