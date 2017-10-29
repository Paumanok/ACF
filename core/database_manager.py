#database class

from pymongo import MongoClient
import json
from bson import objectid

class dbm:

    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')

        #db
        self.db = self.client['ACF_db']

        #collections
        self.pets = self.db['pets']
        self.feedlogs = self.db['feedlogs']

    def insert(self, collection, entry):
        #get dict of object
        entry_dict = entry.__dict__
        #insert into appropriate collection
        entry.db_id = collection.insert_one(entry_dict).inserted_id
        print("i just got this id " )
        print(entry.db_id)

    def update(self, collection, entry):
        #collection.updateOne()
        #replacing with updated python object might be easier
        return

    def replace(self, collection, entry):
        something = collection.replace_one({"_id":entry.db_id}, entry.__dict__)
        print(something)

    def get_by_id(self, collection, entry):
        return collection.find_one({"_id": str(entry.db_id)})

    def get_by_name(self, collection, name):
        return collection.find_one({"name": name});

