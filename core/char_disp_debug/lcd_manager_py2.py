#/usr/bin/python

#author: Matthew Smith
#some code used from Adafruit char_lcd examples

from subprocess import *
from time import sleep, strftime, time
from datetime import datetime
from Queue import *
import signal
import Adafruit_CharLCD as LCD
import ipclock
import threading


#manange queue of messages
#runs the main display loop in separate
#thread while messages can be added
#to the display queue
#
#If no messages are queued up to display,
#it will just display clock&IP
class display_queue:
    
    def  __init__(self):
        self.clock = ipclock.ipclock()
        self.lcd = LCD.Adafruit_CharLCDPlate()
        self.message_queue = Queue()       
        self.message_queue.put(lambda:self.clock.display())
        run_thread = threading.Thread(target=self.run, args=())
        run_thread.daemon = True
        run_thread.start()
    
    #gets messages off queue and displays for 10 seconds
    #if queue is empty, it will re-add the default message(ipclock)
    def run(self):    
        while(True):    
            message = self.message_queue.get(True)
            if(self.message_queue.empty()):
                self.message_queue.put(lambda:self.clock.display())

            start_time = time()
            self.lcd.clear()
            while(time() - start_time < 10):
                message()
            self.lcd.clear()
            start_time = time()

    #generic higher level string formatting
    #probably shouldnt be in here but it works
    def display_string(self, inputString):
        self.lcd.set_cursor(0,0)
        if(len(inputString) <= 16):
            self.lcd.message(inputString)
        elif(32 > len(inputString) > 16):
            self.lcd.message(inputString[0:15])
            self.lcd.message(inputString[16:])
        elif(len(inputString) > 32):
            self.lcd.autoscroll(True);
            self.lcd.message(inputString);
            self.lcd.autoscroll(False);
        else:
            self.lcd.message("error displaying message")
    
    #add message to queue
    def add_string(self, inputString):
        self.message_queue.put( lambda:self.display_string(inputString))



