#RFID utility
#Author:Matthew Smith

import signal
import time
import sys
from pirc522 import RFID

class RFID_util():

    def __init__(self):
        self.reader = RFID()
        self.util = self.reader.util()
        self.run = True

    def end_read(self, signal, frame):
        global run
        self.run = False
        self.reader.cleanup()
        sys.exit()

    def read(self):

        while self.run:
            self.reader.wait_for_tag()

            (error, data) = self.reader.request()
            if not error:
                print("\nDetected: " + format(data, "02x"))

            (error, uid) = self.reader.anticoll()
            if not error:
                #read some info
                #put read into queue
            time.sleep(1)
