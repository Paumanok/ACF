#application server for running servos and junk
#author: matthew smith
import time
import sys
import signal
class app_serv():

    def __init__(self, queue):
        self.rfid_queue = queue

    def print_queue(self):
        while True:
            if self.rfid_queue.empty():
               time.sleep(1)
            else:
                print("\n\nPrinting from application server")
                print(self.rfid_queue.get(True))

