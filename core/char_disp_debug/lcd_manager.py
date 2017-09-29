#/usr/bin/python

#author: Matthew Smith
#some code used from Adafruit char_lcd examples

from subprocess import *
from time import sleep, strftime
from datetime import datetime
from Queue import *
import time
import signal
import Adafruit_CharLCD as LCD
import ipclock
import thread

lcd = LCD.Adafruit_CharLCDPlate()



#manange queue of messages
#runs the main display loop in separate
#thread while messages can be added
#to the display queue
#
#If no messages are queued up to display,
#it will just display clock&IP
class display_queue(self):
    
    def  __init__(self):
        self.message_queue = Queue()
        self.clock = ipclock()
        self.message_queue.put(lambda:self.clock.display())
        run_thread = thread.start_new_thread(self.run)
    
    #gets messages off queue and displays for 10 seconds
    #if queue is empty, it will re-add the default message(ipclock)
    def run(self):    
        while(True):    
            message = self.message_queue.get(True)
            if(self.message_queue.empty());
                self.message_queue.put(lambda:self.clock.display())

            start_time = time.time()
            lcd.clear()
            while(time.time() - start_time < 10):    
                message()
            lcd.clear()
            start_time = time.time()

    #generic higher level string formatting
    #probably shouldnt be in here but it works
    def display_string(self, inputString):
        lcd.set_cursor(0,0)
        if(inputString.length() <= 16):
            lcd.message(inputString)
        elif(32 > inputString.length() > 16):
            lcd.message(inputString[0:15])
            lcd.message(inputString[16:])
        elif(inputString.length() > 32):
            lcd.autoscroll(True);
            lcd.message(inputString);
            lcd.autoscroll(False);
        else:
            lcd.message("error displaying message")
    
    #add message to queue
    def add_string(self, inputString):
        self.message_queue.put(lambda:self.display_string(inputString))



