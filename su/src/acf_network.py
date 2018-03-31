import urequests as r
import esp
import network

newkey_key = "CanIHasCheezeburger"

class acf_network:
    def __init__(self,DEBUG=False):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.connect()
        self.DEBUG = DEBUG
        self.connected = False

    def connect(self):
        self.wlan.connect('TestKitters','FeedUrKatz')

    def isConnected(self):
        if self.wlan.status() == network.STAT_GOT_IP and self.connected == False:
            self.connected = True
            if self.DEBUG == True:
                print("connected")
                print( self.wlan.ifconfig() )
        elif self.wlan.status() != network.STAT_GOT_IP:
            self.connected = False
            if self.DEBUG == True:
                print("connection status: %d", self.wlan.status())
        return self.connected

    # Checks to see if the stored key is valid with the pi server
    def verifyKey(self, key):
        resp = r.get('http://'+self.wlan.ifconfig()[2]+":5000/sfeeder/config",json = {'key':key}, headers={'Content-Type':'application/json'})
        b = resp.json()['bool']
        return b

    def getNewKey(self):
        resp = r.post('http://'+self.wlan.ifconfig()[2]+":5000/sfeeder/config", json = {'id':esp.flash_id(), 'key': newkey_key}, headers={'Content-Type':'application/json'})
        b = resp.json()['bool']
        key = resp.json()['key']
        return (b, key)

    def canIFeed(self, tag, key):
        resp = r.post()
        b = resp.json()['bool']
        serv = res.json()['serv']
        return (b,serv)

    def petFed(self, tag, key, base_wt):
        resp = r.post()

