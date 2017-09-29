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


debug = False

class ipclock:
    
    def __init__(self):    
        self.ipaddr_cmd = "ip addr show wlan0 | grep  'inet ' | awk '{print $2}' | cut -d/ -f1"
        self.ipaddr = ""

    def run_cmd(self):
        p = Popen(self.ipaddr_cmd, shell=True, stdout=PIPE)
        self.ipaddr = p.communicate()[0]

    def display(self):
        #am/pm time string ('%b %d %I:%M %p\n')
        self.run_cmd()
        lcd.set_cursor(0,0)
        lcd.message(datetime.now().strftime('%b %d  %I:%M:%S\n'))
        lcd.message('IP %s\n' % (self.ipaddr))


def main():
    clock = ipclock()
    while True:
        clock.display()


if __name__ == "__main__":
    main()

