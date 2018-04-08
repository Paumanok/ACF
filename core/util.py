import time
from datetime import datetime
from database_manager import dbm

num_to_day = {0:"M", 1:"T", 2:"W", 3:"R", 4:"F", 5:"S", 6:"U"}

db = dbm().db

NULL_WEIGHT = -1

#can pet feed: logic to see if a pet is valid and if current time 
#is between one of allowed feed time tuples
def can_pet_feed( uid_string, f_id):
    #check the time and see if it's cool to feed
    print(uid_string)
    pet = db.pets.find_one({"tag_id":uid_string,"feeder_id":f_id})
    if pet is not None:
        print(pet["name"])
        print("uid: "+ uid_string)
        cur_time = int(time.strftime("%l%M"))
        today = num_to_day[datetime.today().weekday()]
        feed_times = pet["feed_times"]
        for t in feed_times[today]:
            if len(t) > 0:
                print(t)
                #if current time is within feedtime bracket
                if cur_time >= t[0] and cur_time <= t[1]:
                    db.feedlogs.insert_one({"name":pet["name"],"datetime":cur_time, "base_wt":NULL_WEIGHT})
                    return True
    return False

#convert_string: converts a list of 16 hex digits into a
#single 16 byte hex string for use in db entry
def convert_string(uid_list):
    uid_string = ""
    for i in uid_list:
        uid_string += str(hex(i)[2:])
    return "0x" + uid_string

#finds an available id for for a feeder
def available_id():
    i = 1
    while db.feeder.find({'id':i}).count() == 1:
        i += 1
    return i
