#database class

from pymongo import mongoClient


class ddm

    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['ACF_db']
        self.collection = self.db['pets']
        self.collect = self.db['feedlogs']

    def insert(self, db_name, entry):
        #i know nothing about db shit

