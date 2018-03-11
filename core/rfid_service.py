#RFID utility
#Author:Matthew Smith

import signal
import time
import sys
from pirc522 import RFID, RFIDUtil
from queue import *

class RFID_util():

    def __init__(self, queue):
        self.reader = RFID()
        self.util = self.reader.util()
        self.run = True
        self.id_queue = queue

    def end_read(self, signal, frame):
        global run
        self.run = False
        self.reader.cleanup()
        sys.exit()

    def read_while(self):

        while self.run:
            self.reader.wait_for_tag()

            (error, data) = self.reader.request()
            if not error:
                print("\nDetected: " + format(data, "02x"))

            (error, uid) = self.reader.anticoll()
            if not error:
                #read some info
                #put read into queue

                #set card uid for util
                self.util.set_tag(uid)
                #we need keys for each keychain, either default at 0xFF or store in db

                self.util.auth(self.reader.auth_a, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
                self.util.do_auth(self.util.block_addr(2,1))
                (error, data) = self.reader.read(9)
                if not error:
                    print(data)
                    self.id_queue.put(data)
                else:
                    print("error hit")
                time.sleep(3)
