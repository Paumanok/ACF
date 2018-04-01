#!/usr/bin/python
#author: matthew smith mrs9107
#file: main.py
#purpose: initalize debugging interfaces
#         check/create db
#         initialize web server
#         initialize application server
#
import threading
import server
from queue import *
from database_manager import dbm
#import char_disp_debug/lcd_manager
from rfid_service import RFID_util
from application_server import app_serv

class ACF():

    def __init__(self):
        self.rfid_read_queue = Queue()
        self.rfid_command_queue = Queue()
        print("initializing database")
        self.dbm = dbm()
        self.rfid = RFID_util(self.rfid_read_queue, self.rfid_command_queue)
        self.apsrv = app_serv(self.rfid_read_queue)

        print("starting services...")
        #threading.Thread(target = server.run_server, args = (self.rfid_command_queue)).start()
        threading.Thread(target = self.rfid.read_while).start()
        threading.Thread(target = self.apsrv.check_for_pet).start()
        server.run_server(self.rfid_command_queue)





if __name__ == "__main__":
    feeder = ACF()
    while True:
        continue

