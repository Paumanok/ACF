import uasyncio as asyncio
import acf_network as a
import mfrc522 as r
import load_sensor as ls
import easydriver_esp as ed
import time

KEYINVALID = -1
NOFEED=0

def do_read( rdr ):
    (stat, tag_type) = rdr.request(rdr.REQIDL)

    if stat == rdr.OK:

        (stat, raw_uid) = rdr.anticoll()

        if stat == rdr.OK:

            if rdr.select_tag(raw_uid) == rdr.OK:

                key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                auth = rdr.auth(rdr.AUTHENT1A, 9, key, raw_uid)
                if auth == rdr.OK:
                    tag = rdr.read(9)
                    rdr.stop_crypto1()

                    uid_string = ""
                    for i in tag:
                        uid_string += str(hex(i)[2:])
                    return (auth,"0x" + uid_string)
                else:
                    return (rdr.NOTAGERR, None)
        
    return (rdr.ERR, None)

class Coroutines:
    def __init__(self,db,DBG=False):
        self.db = db
        self.DEBUG = DBG
        self.net = a.acf_network(DEBUG=self.DEBUG)
        self.rfid = r.MFRC522(2,15,spiblk=1)
        self.motor = ed.Motor(None,None,0,4,800,50)
        self.load = ls.LoadSensor()
        self.key_verified = False
        self.pet_detected = False
        self.feed = False
        self.base_wt = None
        self.feed_wt = None
        self.weightcheck = 0

    async def networkRoutine(self):
        while True:
            await asyncio.sleep(.5)
            if self.net.isConnected() and self.key_verified == False:
                try:
                    if self.net.verifyKey(self.db.getKey()) == False:
                        (b, key) = self.net.getNewKey()
                        if b == True:
                            self.key_verified = True
                            self.db.setKey(key)
                    else:
                        self.key_verified = True
                except OSError as e:
                    if self.DEBUG == True:
                        print("Error during during key evaluation due to :", e)
                        await asyncio.sleep(5)
            elif self.net.isConnected() == False:
                self.key_verified = False

    async def petRoutine(self):
        while True:
            await asyncio.sleep(.3)
            if self.key_verified == True and self.feed == False:
                (auth, tag) = do_read(self.rfid)
                if tag != None:
                    self.pet_detected = True
                    if self.DEBUG:
                        print("Pet detected: ", tag)
                else:
                    self.pet_detected = False
            elif self.key_verified == False:
                self.pet_detected = False

            if self.pet_detected == True:
                if self.feed == False:
                    try:
                        val = self.net.canIFeed(self.db.getKey(),tag)
                    except OSError as e:
                        print("Feed permission error due to :",e)
                        val = KEYINVALID
                    if val == KEYINVALID:
                        self.key_verified = False
                    elif val > NOFEED:
                        self.feed = True
                        self.feed_wt = val
                        self.tag = tag
                        self.motor.driveOn()

    async def dispenseRoutine(self):
        while True:
            await asyncio.sleep(.5)
            if self.feed == True:
                if self.base_wt == None:
                   self.base_wt = self.load.getGram()

                if self.load.isLoadValid(ls.loadCheck(self.feed_wt) or self.weightcheck == 100):
                    self.motor.driveOff()
                    self.weightcheck = 0
                    try:
                        self.net.petFed(self.tag,self.base_wt)
                        if self.DEBUG :
                            print("Pet food dispensed: ",self.feed_wt-self.base_wt)
                            print("Pet food weight:    ", self.feed_wt)
                            print("Base food weight:   ", self.base_wt)
                        self.feed = False
                        self.base_wt = None
                        self.feed_wt = None
                    except OSError as e:
                        if self.DEBUG:
                            print("Error Communicating finished feeding to feeder due to :", e)
                elif (self.weightcheck+1)%10 == 0 and self.load.isJammed() :
                    i = 6
                    while (i >= 1):
                        self.motor.setDir(i%2)
                        time.sleep(1)
                        i-=1
                    self.weightcheck = 0
                else :
                    self.weightcheck +=1
