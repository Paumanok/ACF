#application server for running stepper and junk
#author: matthew smith
import time
from datetime import datetime
import sys
import signal
import threading
from queue import *
from database_manager import dbm
from bson import objectid
from easydriver.easydriver_pi import Motor
from hx711 import LoadSensor, FULL, JAMMED, FEEDING
from util import can_pet_feed, convert_string,log_feed


MASTER_FEEDER_ID = 1

# Determine if JAMMING or if empty
EMPTYCOUNT = 10
# Make count even and greater than 0
JIG_COUNT = 6
JIG_HALF_PERIOD = 1

class app_serv():

    def __init__(self, queue):
        mp = {"m1":11, "m2":13, "dir":12, "step":16} #motor pins
        self.rfid_queue = queue
        self.weighing = False
        self.motor = Motor(mp["m1"], mp["m2"], mp["dir"], mp["step"])
        self.motor.setFreq(800)
        self.motor.setDuty(50)
        self.motor.setDir(1)
        self.motor.setStepMode(3)
        self.load_sensor = LoadSensor()
        self.emptycnt = 0

    #tests functionality of inter-thread command queue
    def print_queue(self):
        while True:
            if self.rfid_queue.empty():
               time.sleep(1)
            else:
                print("\n\nPrinting from application server")
                print(self.rfid_queue.get(True))

    def check_for_pet(self):
        db = dbm()
        while True:
            if self.rfid_queue.empty():
                time.sleep(1)
            else:
                uid_list = self.rfid_queue.get(True)
                uid_string = convert_string(uid_list)
                pet = can_pet_feed(uid_string, MASTER_FEEDER_ID)
                if pet != None:
                    print("feeding")
                    self.feed(pet)

    #feed: initializes weighing loop in second thread and checks
    #the weighing status as more food is added.
    #stops motors when desired amount is reached
    #param: pet--pet dictionary pulled from database
    def feed(self, pet):
        weight_queue = Queue()#queue for holding weights from different thread
        food_amt = pet["food_quantity"] #get allowed amount
        baseweight = self.load_sensor.getGram()#weight_queue.get()#get first weight
        self.motor.driveOn()
        while (1):
            load_state = self.load_sensor.loadState(food_amt)
            if (load_state == JAMMED):
                self.emptycnt += 1
                self.jig()
            elif (load_state == FULL):
                self.emptycnt = 0
                break
            if(self.emptycnt == EMPTYCOUNT):
                break;
            self.emptycnt = 0

        self.motor.driveOff()
        self.weighing = False #stop weighing thread
        log_feed(pet,baseweight)
        print("finished feeding")

        if (self.emptycnt == EMPTYCOUNT):
            print("refill feeder")

    def jig(self):
        i = JIG_COUNT
        while(i >= 1):
            self.motor.setDir(i%2)
            i -= 1
            time.sleep(JIG_HALF_PERIOD)

    #attempt to clear jams with rapid back and forth movement.
    def stall_dance():
        self.motor.driveOn()
        for i in range(10):
            if i % 2:
                self.motor.setDir(1)
            else:
                self.motor.setDir(0)
            sleep(.2)

        self.motor.setFreq(800)
        self.motor.setDuty(50)
        self.motor.setDir(1)
        self.motor.setStepMode(0)

