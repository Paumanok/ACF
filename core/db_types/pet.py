#pet class for automatic cat feeder

class pet:
    #db_id = None
    tag_id = None

    def __init__(self, name, age, weight, quantity):
        self.name = name
        self.age = age
        self.weight = weight
        self.food_quantity = quantity

        #this should just be a list of 24hr times that would normally repeat daily
        #kiss: no colon, 4 digit number, 0100 = 1:00 am, 2300 = 11:00pm
        #self.feed_times = feed_times
        #new route: dictionary of days of the week, containing list of 2 item lists defining windows
        #ie "M":[(1300, 1500), (1800, 2000)]
        self.feed_times = {"M": [],
                           "T": [],
                           "W": [],
                           "R": [],
                           "F": [],
                           "S": [],
                           "U": []
                           }

    #if pet is embedded in dict, this overrides
    #default to string method
    def __str__(self):
        return self.__dict__
