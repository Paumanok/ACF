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

    def read_while(self):

        while self.run:

            #check if theres a write command that needs attention
            #maybe needs to be lower down, read_while might need to be more generic
            if not self.cmd_queue.empty():
                write_id(self.cmd_queue.get())

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

                (error, data) = self.reader.read(9)
                if not error:
                    #print(data)
                    self.id_queue.put(data)
                else:
                    print("RFID read error, try again")
                time.sleep(3)


        def write_id(self, pet):
            short_name = pet['name'][:16]
            weight = pet['weight']
            uid = 0
            for c in short_name:
                uid = (uid << 16) + ord(c)

            uid = uid & weight
            print(uid)


#something here to run when program receives a sigkill
