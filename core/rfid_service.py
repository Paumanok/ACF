#RFID utility
#Author:Matthew Smith

import signal
import time
import sys
from pirc522 import RFID, RFIDUtil
from queue import *

class RFID_util():

    def __init__(self, read_queue, command_queue):
        self.reader = RFID()
        self.util = self.reader.util()
        self.run = True
        self.id_queue = read_queue
        self.cmd_queue = command_queue

    def end_read(self, signal, frame):
        global run
        self.run = False
        self.reader.cleanup()
        sys.exit()

    #read_while: polling loop with rfid device
    #will check write queue and when non empty,
    #will execute write of queue item instead of
    #reading.
    def read_while(self):

        while self.run:

            self.reader.wait_for_tag()

            (error, data) = self.reader.request()
            if not error:
                print("\nDetected: " + format(data, "02x"))

            (error, uid) = self.reader.anticoll()
            if not error:

                #set card uid for util
                self.util.set_tag(uid)

                #we need keys for each keychain, either default at 0xFF or store in db
                self.util.auth(self.reader.auth_a, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
                self.util.do_auth(self.util.block_addr(2,1))

                #since this is where we auth'd
                block = 9
                #check if theres a write command that needs attention
                if not self.cmd_queue.empty():
                    self.reader.write(block, self.cmd_queue.get())
                    print("tag written")
                else:
                    (error, data) = self.reader.read(block)
                    if not error:
                        #print(data)
                        self.id_queue.put(data)
                    else:
                        print("RFID read error, try again")
                time.sleep(3)
                util.deauth()



#something here to run when program receives a sigkill
