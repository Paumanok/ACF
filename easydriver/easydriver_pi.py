import RPi.GPIO as rg

rg.setmode(rg.BCM)

class MotorPin:
    def __init__(self, m1, m2, dir, step, freq=50, duty=0):
        # Initialize Pins for proper operation
        self.m1 = m1
        rg.setup(m1,rg.OUT)
        self.m2 = m2
        rg.setup(m2,rg.OUT)
        self.dir = dir
        rg.setup(dir, rg.OUT)
        rg.setup(step,rg.OUT)
        self.drive = PWM(Pin(step),freq)

        # Store duty cycle and set GPIO pins to 0
        self.duty = duty
        rg.output(m1,0)
        rg.output(m2,0)
        rg.output(dir,0)

    def setDuty(self, duty):
        self.duty = duty
        self.drive.ChangeDutyCycle(duty)

    def setFreq(self, freq):
        self.drive.ChangeFrequency(freq)

    def setStepMode(self, mode):
        if 0 <= mode and mode <= 3:
            rg.output(m1,(1&mode))
            rg.output(m2,1&(mode>>1))

    def setDir(self,dir):
        if 0 == dir or 1 == dir:
            rg.output(self.dir,(dir))

    def driveOn(self):
        self.drive.start(self.duty)

    def driveOff(self):
        self.drive.stop()
