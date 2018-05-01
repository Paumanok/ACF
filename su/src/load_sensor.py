import os
if os.__name__ == 'uos':
    from hx711_esp_pin import DTPin, SCKPin
else :
    from hx711_pi_pin import DTPin, SCKPin

# Gram Conversion Value
scale = 743.0

class LoadSensor:
    def __init__(self):
        self.dt = DTPin()
        self.sck = SCKPin()

        # Make sure sck is off
        self.sck.off()
        if self.sck.value() != 0:
            raise("Hardware malfunction sck is not changing value")
        self.__offset = 0
        self.calibrate()
        self.calibrate()

    # Get 24 bit weight value
    def getValue(self):
        # Initalize base reading value
        reading = 0x0

        # Check for available value
        while self.dt.value() != 0:
            pass

        # Shift in the 24 bit value
        for i in range(24):
            self.sck.pulse()
            reading = (reading << 1) | self.dt.value()

        # 25th pulse for setting 128 gain
        self.sck.pulse()

        # XOR to clear sign bit
        return reading ^ 0x800000

    # Get an average of the weight readings
    def getAvgValue(self, avg_cnt = 10):
        sum = 0
        cnt = avg_cnt
        while cnt > 0:
            sum += self.getValue()
            cnt -= 1

        return sum / avg_cnt

    def getGram(self, avg_cnt = 10):
        weight = self.getAvgValue(avg_cnt) - self.__offset
        return weight / scale

    def calibrate(self, avg_cnt= 1):
        self.__offset = self.getAvgValue(avg_cnt)
