import os
if os.__name__ == 'uos':
    from hx711_esp_pin import DTPin, SCKPin
else :
    from hx711_pi_pin import DTPin, SCKPin
from array import array

# Gram Conversion Value
scale = 743.0
# reading buffer size
buffer_size = 5
valid_buf_cnt = int(buffer_size * .8)

class LoadSensor:
    def __init__(self):
        self.dt = DTPin()
        self.sck = SCKPin()
        self.buf = array('q',[0]*buffer_size)
        self.bufi = 0
        self.bufuse = 0

        # Make sure sck is off
        self.sck.off()
        if self.sck.value() != 0:
            raise("Hardware malfunction sck is not changing value")
        self.__weight_offset = 0
        self.__offset = 0
        self.calibrate()

    def __buf_add__(self,val):
        self.buf[self.bufi] = val
        if self.bufi < buffer_size - 1:
            self.bufi += 1
        else:
            self.bufi = 0

    def __buf_check__(self, lf):
        cnt = 0
        for bval in self.buf:
            if lf(bval):
                cnt += 1
        if cnt == valid_buf_cnt:
            self.bufuse = 0
            return True
        else :
            return False

    def __buf_avg__(self, lf):
        total = 0
        for bval in self.buf:
            if lf(bval):
                total += bval
        return int(bval/buffer_size)

    def __load_verify__(self, lf):
        while self.bufuse < buffer_size - 1 :
            val = self.getValue() - self.__offset
            self.__buf_add__(val)
            self.bufuse += 1
        val = self.getValue() - self.__offset
        self.__buf_add__(val)
        return self.__buf_check__(lf)

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

    def getGram(self, lf):
        if(self.__buf_check__(lf)):
            return self.__buf_avg__(lf)/scale
        else:
            return -1

    def gramToLoadVal(self, weight):
        return int(weight*scale)

    def isLoadValid(self, lf):
        return self.__load_verify__(lf)

    def calibrate(self,avg_cnt=5):
        self.__offset = int(self.getAvgValue(avg_cnt))
        # Checks to see if 80% of the buffer values are within the
        # tolerable offset of 100 before gram conversion. Most values
        # seem to fall within this tolerance which equates to about a
        # .13 Gram offset from the 0 reading
        while self.__load_verify__(lambda x: abs(x)<100):
            self.__offset = int(self.getAvgValue(avg_cnt))
