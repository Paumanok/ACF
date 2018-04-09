import uasyncio as asyncio
import acf_network as a
import mfrc522 as r
import load_sensor as ls
import easydriver_esp as ed

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
        self.motor = ed.Motor(None,None,0,4,500,50)
        self.load = ls.LoadSensor()
        self.key_verified = False
        self.pet_detected = False
        self.feed = False
        self.base_wt = None
        self.feed_wt = None

    async def networkRoutine(self):
        while True:
            await asyncio.sleep(.5)
            if self.net.isConnected() and self.key_verified == False:
                if self.net.verifyKey(self.db.getKey()) == False:
                    (b, key) = self.net.getNewKey()
                    if b == True:
                        self.key_verified = True
                        self.db.setKey(key)
                else:
                    self.key_verified = True

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
                    val = self.net.canIFeed(self.db.getKey(),tag)
                    if val == KEYINVALID:
                        self.key_verified = False
                    elif val > NOFEED:
                        self.feed = True
                        self.feed_wt = val
                        self.motor.driveOn()
                    
                    if self.DEBUG:
                        print("Feed dispense val: ", val)

    async def dispenseRoutine(self):
        while True:
            await asyncio.sleep(.5)
            if self.feed == True:
                if self.base_wt == None:
                   self.base_wt = self.load.getGram()

                if self.isLoadValid(ls.loadCheck(self.feed_wt)):
                    self.motor.driveOff()
                    self.net.petFed(tag,key,self.base_wt)
                    if self.DEBUG :
                        print("Pet food dispensed: ",self.feed_wt-self.base_wt)
                        print("Pet food weight:    ", self.feed_wt)
                        print("Base food weight:   ", self.base_wt)
                    self.feed = False
                    self.base_wt = None
                    self.feed_wt = None
