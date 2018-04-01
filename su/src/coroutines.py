import uasyncio as asyncio
import acf_network as a
import mfrc522 as r
import load_sensor as ls
import easydriver_esp as ed

import network


def do_read( rdr ):
    (stat, tag_type) = rdr.request(rdr.REQIDL)

    if stat == rdr.OK:

        (stat, raw_uid) = rdr.anticoll()

        if stat == rdr.OK:
            #print("New card detected")
            #print("  - tag type: 0x%02x" % tag_type)
            #print("  - uid     : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
            #print("")

            if rdr.select_tag(raw_uid) == rdr.OK:

                key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                
                auth = rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid)
                if auth == rdr.OK:
                    tag = rdr.read(8)
                    #print("Address 8 data: %s" % rdr.read(8))
                    rdr.stop_crypto1()
                    return (auth,tag) 
                else:
                    return(rdr.NOTAGERR, None)
            else:
                    return (rdr.ERR, None)

class Coroutines:
    def __init__(self,db):
        self.db = db
        self.net = a.acf_network(DEBUG=True)
        self.rfid = r.MFRC522(2,16,spiblk=1)
        self.motor = ed.Motor(None,None,0,15,500,50)
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
                auth, tag = do_read(self.rfid)
                if tag != None:
                    self.pet_detected = True
                else:
                    self.pet_detected = False
            elif self.key_verified == False:
                self.pet_detected = False
            
            if self.pet_detected == True:
                (b, serv) = self.net.canIFeed(tag,)
                self.feed = b
                if b:
                    self.feed_wt = serv * .95

    async def dispenseRoutine(self):
        while True:
            await asyncio.sleep(.5)
            if self.feed == True:
                wt = self.load.getGram(1)
                if self.base_wt == None:
                   self.base_wt = wt
                
                if self.feed_wt <= wt:
                    self.net.petFed(tag,key,self.base_wt)
                    self.feed = False
                    self.base_wt = None
                    self.feed_wt = None
