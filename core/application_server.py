#application server for running stepper and junk
#author: matthew smith
import time
import datetime
import sys
import signal
import threading
from database_manager import dbm
from bson import objectid
from easydriver/easydriver_py import Motor
from hx711/load_sensor import LoadSensor

class app_serv():

    num_to_day = {0:"M", 1:"T", 2:"W", 3:"R", 4:"F", 5:"S", 6:"U"}

    def __init__(self, queue):
        self.rfid_queue = queue
        self.weighing = False
        self.motor = Motor(m1, m2, dir, step)
        self.load_sensor = LoadSensor()
        self.load_sensor.calibrate() #set it up

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
                pet = pets.find_one({"tag_id":uid_string})
                if pet is not None:
                    if check_time(pet):
                        self.feed(pet)
                    else:
                        pass


    def check_time(self, pet):
        #check the time and see if it's cool to feed
        cur_time = int(time.strftime("%l%M"))
        today = num_to_day[datetime.today().weekday()]
        feed_times = pet["feed_times"]
        for t in feed_times[today]
            if len(t) > 0:
                for i in val:
                    #if current time is within feedtime bracket
                    if cur_time >= i[0] and cur_time <= i[1]:
                        return True
        return False

    def feed(self, pet):
        weight_queue = Queue()#queue for holding weights from different thread
        self.weighing = True #flag for weigh_while
        food_amt = pet["food_quantity"] #get allowed amount
        #start weigh_while thread
        threading.Thread(target = self.weigh_while, args = weight_queue).start()
        cur_weight = weight_queue.get()#get first weight
        self.motor.driveOn()
        while cur_weight < food_amt:
            cur_weight = weight_queue.get()
        self.motor.driveOff()
        self.weighing = False #stop weighing thread


    def weigh_while(self, weight_queue):
        while self.weighing:
            weight = self.load_sensor.getGram()
            weight_queue.add(weight)
            time.sleep(1)

    def convert_string(self, uid_list):
        uid_string = ""
        for i in uid_list:
            uid_string += str(hex(i)[2:])
        return "0x" + uid_string
