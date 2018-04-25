from machine import Pin, PWM

def getDuty(duty):
    if 0 <= duty and duty <= 100:
        return int(1023 * duty/100)
    else:
        return 0

class Motor:
    def __init__(self, m1, m2, dir, step, freq=50, duty=0):
        
        if m1 != m2:
            self.m1 = Pin(m1,Pin.OUT)
            self.m2 = Pin(m2,Pin.OUT)
            self.m1.value(0)
            self.m2.value(0)
        else:
            self.m1 = -1
            self.m2 = -1
        self.dir = Pin(dir,Pin.OUT)
        self.drive = PWM(Pin(step),freq,0)
        self.duty = getDuty(duty)
        self.dir.value(1)

#    def setDuty(self, duty):
#        self.duty = duty
#        self.drive.duty(duty)
#
#    def setFreq(self, freq):
#        self.drive.freq(freq)
#
#    def setStepMode(self, mode):
#        if 0 <= mode and mode <= 3:
#            self.m1.value(1&mode)
#            self.m2.value(1&(mode>>1))

    def setDir(self,dir):
        if 0 == dir or 1 == dir:
            self.dir.value(dir)

    def driveOn(self):
        self.drive.init()
        self.drive.duty(self.duty)

    def driveOff(self):
        self.drive.deinit()
