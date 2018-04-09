import urequests as r
import esp
import network
import time

newkey_key = "CanIHasCheezeburger"
KEYINVALID = -1
NOFEED=0
RECNT=1000

class acf_network:
    def __init__(self,DEBUG=False,SSID='ACF',SSIDKEY='FeedUrKatz'):
        self.wlan = network.WLAN(network.STA_IF)
        self.SSID = SSID
        self.SSIDKEY = SSIDKEY
        self.wlan.active(True)
        self.connect()
        self.DEBUG = DEBUG
        self.connected = False
        self.recnt = 0

    def connect(self):
        self.wlan.connect(self.SSID,self.SSIDKEY)

    def isConnected(self):
        if self.wlan.status() == network.STAT_GOT_IP and self.connected == False:
            self.connected = True
            print("connected")
        elif self.wlan.status() != network.STAT_GOT_IP:
            self.connected = False
            if self.recnt < RECNT:
                self.recnt+=1
            else:
                if self.DEBUG == True:
                    print("Reconnect attempted")
                self.wlan.disconnect()
                time.sleep(5)
                self.connect()
                self.recnt=0
                if self.DEBUG == True:
                    print("connection status: ", self.wlan.status())

        if(self.DEBUG==True and self.connected == True):
            print(self.wlan.ifconfig())

        return self.connected

    # Checks to see if the stored key is valid with the pi server
    def verifyKey(self, key):
        resp = r.get('http://'+self.wlan.ifconfig()[2]+":5000/sfeeder/config",json = {'key':key}, headers={'Content-Type':'application/json'})
        b = resp.json()['bool']
        if self.DEBUG :
            print("Key verified as: ", b)
        return b

    def getNewKey(self):
        resp = r.post('http://'+self.wlan.ifconfig()[2]+':5000/sfeeder/config', json = {'id':esp.flash_id(), 'key': newkey_key}, headers={'Content-Type':'application/json'})
        b = resp.json()['bool']
        key = resp.json()['key'].encode('utf-8')
        if self.DEBUG :
            print("New key given: ", b)
        return (b, key)

    def canIFeed(self, key, tag):
        resp = r.get('http://'+self.wlan.ifconfig()[2]+':5000/sfeeder/feed', json = {'key':key, 'tag_id':tag }, headers={'Content-Type':'application/json'})
        feed = resp.json()['feed']
        if self.DEBUG :
            print("Feed value: ", feed)
        return feed

    def petFed(self, key, tag, base_wt):
        resp = r.post('http://'+self.wlan.ifconfig()[2]+':5000/sfeeder/feed', json = {'key':key, 'tag_id':tag, 'base_wt':base_wt}, headers={'Content-Type':'application/json'})
        return

