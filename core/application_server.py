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
from hx711.load_sensor import LoadSensor
class app_serv():

    num_to_day = {0:"M", 1:"T", 2:"W", 3:"R", 4:"F", 5:"S", 6:"U"}

    def __init__(self, queue):
        mp = {"m1":11, "m2":13, "dir":12, "step":16} #motor pins
        self.rfid_queue = queue
        self.weighing = False
        self.motor = Motor(mp["m1"], mp["m2"], mp["dir"], mp["step"])
        self.motor.setFreq(400)
        self.motor.setDuty(50)
        self.load_sensor = LoadSensor()
        self.load_sensor.calibrate() #set it up

    #tests functionality of inter-thread command queue
    def print_queue(self):
        while True:
            if self.rfid_queue.empty():
               time.sleep(1)
            else:
                print("\n\nPrinting from application server")
                print(self.rfid_queue.get(True))

    def check_for_pet(self):
        db = dbm().db
        pets = dbm().pets
        while True:
            if self.rfid_queue.empty():
                time.sleep(1)
            else:
                uid_list = self.rfid_queue.get(True)
                uid_string = self.convert_string(uid_list)
                print(uid_string)
                pet = pets.find_one({"tag_id":uid_string})
                if pet is not None:
                    print(pet["name"])
                    if self.check_time(pet):
                        print("uid: "+ uid_string)
                        print("feeding")
                        self.feed(pet)

                    else:
                        pass

    #check time: logic to see if current time is between one of
    #allowed time tuples
    def check_time(self, pet):
        #check the time and see if it's cool to feed
        cur_time = int(time.strftime("%l%M"))
        today = self.num_to_day[datetime.today().weekday()]
        feed_times = pet["feed_times"]
        for t in feed_times[today]:
            if len(t) > 0:
                print(t)
                #if current time is within feedtime bracket
                if cur_time >= t[0] and cur_time <= t[1]:
                    return True
        return False

    #feed: initializes weighing loop in second thread and checks
    #the weighing status as more food is added.
    #stops motors when desired amount is reached
    #param: pet--pet dictionary pulled from database
    def feed(self, pet):
        weight_queue = Queue()#queue for holding weights from different thread
        self.weighing = True #flag for weigh_while
        food_amt = pet["food_quantity"] #get allowed amount
        #start weigh_while thread
        threading.Thread(target = self.weigh_while, args = [weight_queue]).start()
        cur_weight = weight_queue.get()#get first weight
        self.motor.driveOn()
        while cur_weight < food_amt:
            cur_weight = weight_queue.get()
        self.motor.driveOff()
        self.weighing = False #stop weighing thread
        print("finished feeding")


    #weigh_while: loops while weighing flag = true
    def weigh_while(self, weight_queue):
        while self.weighing:
            weight = self.load_sensor.getGram()
            weight_queue.put(weight)
            time.sleep(1)

    #convert_string: converts a list of 16 hex digits into a
    #single 16 byte hex string for use in db entry
    def convert_string(self, uid_list):
        uid_string = ""
        for i in uid_list:
            uid_string += str(hex(i)[2:])
        return "0x" + uid_string
