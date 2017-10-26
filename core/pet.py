#pet class for automatic cat feeder


class pet:

    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight

    def store_to_db(self):
        #should this be here?
