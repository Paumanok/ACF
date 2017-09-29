#!/usr/bin/python

#author: Matthew Smith
#some code used from Adafruit char_lcd examples

from subprocess import *
from time import sleep, strftime
from datetime import datetime
import time
import signal
import Adafruit_CharLCD as LCD
import weatherfetch

lcd = LCD.Adafruit_CharLCDPlate()

first_run = True


buttons = ((LCD.SELECT,0), (LCD.LEFT,1), ( LCD.UP,2), ( LCD.DOWN,3),  (LCD.RIGHT, 4))

first_page = 0
page_max = 3
page_min = 0

pages = { 0 : lambda clock, Weather: home(clock, Weather),
          1 : lambda: ip_clock(),
          2 : lambda: weather(),
          3 : lambda: page_two() }


debug = False



class weather:

    weather_data = {}
    refresh_rate = 12

    def init(self):
        self.fetch()
        signal.signal(signal.SIGALRM, self.refresh)
        signal.alarm(self.refresh_rate * 60)

    def refresh(self, ignum, frame):
        self.fetch()
        signal.alarm(self.refresh_rate * 60)

    def fetch(self):

        old_alarm = signal.signal(signal.SIGALRM, self.refresh)
        try:
            signal.alarm(10)
            self.weather_data = weatherfetch.get_weather()
        except Alarm:
            print("url fetch timed out")
        finally:
            signal.signal(signal.SIGALRM, old_alarm)
        
        

    def timeout_handler(signum, frame):
        return

    def display(self):
        lcd.set_cursor(0,0)
        lcd.message("Current Temp:\n" + str(self.weather_data['temp_f']) + " Fahrenheit")
        sleep(4)


class ipclock:
    ipaddr_cmd = "ip addr show wlan0 | grep  'inet ' | awk '{print $2}' | cut -d/ -f1"
    ipaddr = ""

    def run_cmd(self):
        p = Popen(self.ipaddr_cmd, shell=True, stdout=PIPE)
        self.ipaddr = p.communicate()[0]

    def display(self):
        #am/pm time string ('%b %d %I:%M %p\n')
        self.run_cmd()
        lcd.set_cursor(0,0)
        lcd.message(datetime.now().strftime('%b %d  %I:%M:%S\n'))
        lcd.message('IP %s\n' % (self.ipaddr))



def home(clock, Weather):
    if(debug):
        print("home ran")
    start_time = time.time()
    lcd.clear()
    while(time.time() - start_time < 10):
        clock.display()
    lcd.clear()
    start_time = time.time()
    while(time.time() - start_time < 5):
        current_minute =  datetime.now().strftime('%M')
        Weather.display()

def page_two():
    lcd.clear()
    lcd.message("page two")



def main():
    Weather = weather()
    clock = ipclock()
    weather.init(Weather)
    page = first_page
    while True:

        pages[page](clock, Weather)
"""
        for button in buttons:
            if lcd.is_pressed(button[0]):
                if button[0] == LCD.UP:
                    page = page + 1
                    if page > page_max:
                        page = page_max
                elif button[0] == LCD.DOWN:
                    page = page - 1
                    if page < page_min:
                        page = page_min
                sleep(.1)
                lcd.clear()
"""

if __name__ == "__main__":
    main()

