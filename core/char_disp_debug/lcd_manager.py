#!/usr/bin/python

#author: Matthew Smith
#some code used from Adafruit char_lcd examples

from subprocess import *
from time import sleep, strftime
from datetime import datetime
import time
import signal
import Adafruit_CharLCD as LCD

lcd = LCD.Adafruit_CharLCDPlate()


class display_queue(self):
    #manange queue of messages
    #add_message
    
