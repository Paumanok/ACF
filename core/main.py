#!/usr/bin/python
#author: matthew smith mrs9107
#file: main.py
#purpose: initalize debugging interfaces
#         check/create db
#         initialize web server
#         initialize application server
#

from queue import *
from database_manager import dbm
#import char_disp_debug/lcd_manager
import server

class ACF():

    def __init__(self):
        print("initializing database")
        self.dbm = dbm()
        print("initializing server")
        server.run_server()





if __name__ == "__main__":
    feeder = ACF()
    while True:
        continue

