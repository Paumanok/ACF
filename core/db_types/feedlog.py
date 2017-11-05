#class for feedlog db types
import datetime

class feedlog:

    def __init__(self, petid):
        self.petid = petid
        self.datetime = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        #short fix for insert checks, datetime shouldnt be the same
        self.name = self.datetime


    def __str__(self):
        return self.__dict__
