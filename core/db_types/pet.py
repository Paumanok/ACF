#pet class for automatic cat feeder

class pet:
    db_id = None;

    def __init__(self, name, age, weight, feed_times = []):
        self.name = name
        self.age = age
        self.weight = weight

        #this should just be a list of 24hr times that would normally repeat daily
        #kiss: no colon, 4 digit number, 0100 = 1:00 am, 2300 = 11:00pm
        self.feed_times = feed_times

    #if pet is embedded in dict, this overrides
    #default to string method
    def __str__(self):
        return self.__dict__
