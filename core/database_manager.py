#database class

from pymongo import MongoClient
import json
from bson import objectid

#print debug flag
debug = False

class dbm:

    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')

        #db
        self.db = self.client['ACF_db']

        #collections
        self.pets = self.db['pets']
        self.feedlogs = self.db['feedlogs']
        self.feeders = self.db['feeders']
    #insert will check for a name and replace instead of insert if cat
    #is there. This must be fixed for other types of db entries
    def insert(self, collection, entry):
        if(len(list(collection.find({"name":entry.name})))==0):
            #get dict of object
            entry_dict = entry.__dict__
            #insert into appropriate collection
            entry.db_id = collection.insert_one(entry_dict).inserted_id
        else:
            if debug: print("replacing instead of inserting")
            self.replace(collection, entry)

    def update(self, collection, entry):
        #collection.updateOne()
        #replacing with updated python object might be easier
        #calling replace for now
        self.replace(collection, entry)

    def replace(self, collection, entry):
        something = collection.replace_one({"name":entry.name}, entry.__dict__)
        print(something)

    def get_by_id(self, collection, entry):
        return collection.find_one({"_id": str(entry.db_id)})

    def get_by_name(self, collection, name):
        return collection.find_one({"name": name});

