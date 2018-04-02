#application server for running servos and junk
#author: matthew smith
import time
import datetime
import sys
import signal
from database_manager import dbm
from bson import objectid
from easydriver/easydriver_py import Motor
from hx711/load_sensor import LoadSensor

class app_serv():

    num_to_day = {0:"M", 1:"T", 2:"W", 3:"R", 4:"F", 5:"S", 6:"U"}

    def __init__(self, queue):
        self.rfid_queue = queue
        self.motor = Motor(m1, m2, dir, step)
        self.load_sensor = LoadSensor()

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
                        #feed
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

    def feed(self, pet);
        #here we're going to use the easy driver and load sensor in unison
        #create queue of weight readings
        #loop load reading in second thread
        #while amount < allowed_amount:
        #run motor
        #kill load sensor reading thread

    def weigh_while(self, weight_queue):
        while True:
            weight = None#weigh
            weight_queue.add(weight)
            time.sleep(1)

    def convert_string(self, uid_list):
        uid_string = ""
        for i in uid_list:
            uid_string += str(hex(i)[2:])
        return "0x" + uid_string
