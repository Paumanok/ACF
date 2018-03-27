from machine import Pin, PWM

class MotorPin:
    def __init__(self, m1, m2, dir, step, freq=50, duty=0):
        self.m1 = Pin(m1,Pin.Out)
        self.m2 = Pin(m2,Pin.Out)
        self.dir = Pin(dir,Pin.Out)
        self.drive = PWM(Pin(dir),freq,0)
        self.duty = duty
        m1.value(0)
        m2.value(0)

    def setDuty(self, duty):
        self.duty = duty
        self.step.duty(duty)

    def setFreq(self, freq):
        self.step.freq(freq)

    def setStepMode(self, mode):
        if 0 <= mode and mode <= 3:
            self.m1.value(1&mode)
            self.m2.value(1&(mode>>1))

    def setDir(self,dir):
        if 0 == dir or 1 == dir:
            self.dir.value(dir)

    def driveOn(self):
        self.drive.init()
        self.drive.duty(self.duty)

    def driveOff(self):
        self.drive.deinit()
