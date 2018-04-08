#author: matthew smith mrs9107
#file: client_new
#purpose: improving on old http server and doing things the "right" way

import requests
from core.db_types.pet import pet


host_addr = "192.168.10.1:5000"


#here we're manually defining the json to pass to the server
new_cat = {"name":"bucky", "age":3, "weight": 10, "feed_times" : []}

#here i'm using my pets db type and converting it to a dict
cat1 = pet(0,"sniffles", 5, 25, 5.5)
cat1.feed_times = {"M":[], "T":[(0000, 2400)], "W":[(0000, 2400)], "R":[(0000, 2400)], "F":[], "S":[], "U":[]}
cat1 = cat1.__dict__
cat2 = pet("fluff", 2, 15, 50).__dict__
cat3 = pet("mango", 4, 12, 50).__dict__


def request_pet_info(thecat):
    name = thecat["name"]
    r = requests.get("http://" + host_addr + "/pets/name/"+ name)
    print(r.status_code)

    print(r.json())


def insert_pet(thecat):
    cat = thecat
    r = requests.post( "http://" + host_addr + "/pets/name/"+ cat["name"], json = cat )
    print(r.status_code)
    #print(r.json())

def config_tag(thecat):
    cat = thecat
    r =  requests.get("http://" + host_addr +"/rfid_config/" + cat["name"])
    print(r.status_code)

def get_all_pets():
    r = requests.get("http://" + host_addr + "/pets/")
    print(r.json())

if __name__ == "__main__":
    cats = [cat1, cat2, cat3]
    for cat in cats:
        insert_pet(cat)
        request_pet_info(cat)
    config_tag(cat1)
    request_pet_info(cat1)
    get_all_pets()
