#application server for running servos and junk
#author: matthew smith
import time
import sys
import signal
from database_manager import dbm
from bson import objectid
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
                if pets.find_one({"tag_id":uid_string}) is not None:
                    #if pet exists, check if it can feed
                    print("pet found in db!")

    def convert_string(self, uid_list):
        uid_string = ""
        for i in uid_list:
            uid_string += str(hex(i)[2:])
        return "0x" + uid_string
