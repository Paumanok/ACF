#author: matthew smith mrs9107
#file: client_new
#purpose: improving on old http server and doing things the "right" way

import requests
from core.db_types.pet import pet


host_addr = "192.168.10.1:5000"


#here we're manually defining the json to pass to the server
new_cat = {"name":"bucky", "age":3, "weight": 10, "feed_times" : []}

#here i'm using my pets db type and converting it to a dict
cat1 = pet("sniffles", 5, 25).__dict__
cat2 = pet("fluff", 2, 15).__dict__
cat3 = pet("mango", 4, 12).__dict__


def request_pet_info():
    r = requests.get("http://" + host_addr + "/pets/name/fluff")
    print(r.status_code)

    print(r.json())


def insert_pet():
    cat = cat2
    r = requests.post( "http://" + host_addr + "/pets/name/"+ cat["name"], json = cat )
    print(r.status_code)
    #print(r.json())

def config_tag():
    cat = cat2
    r =  requests.get("http://" + host_addr +"/rfid_config/" + cat["name"])
    print(r.status_code)


if __name__ == "__main__":
    insert_pet()
    request_pet_info()
    config_tag()
    request_pet_info()
