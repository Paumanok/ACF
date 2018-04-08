#class for feedlog db types
import datetime

class feedlog:

    def __init__(self, name, base_wt, dt):
        self.petname = name
        self.base_wt = base_wt
        self.datetime = dt#'{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

    def __str__(self):
        return self.__dict__
