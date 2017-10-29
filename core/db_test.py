#testing functions to db shiz

from database_manager import dbm
from pet import pet

def main():
    my_dbm = dbm()
    pets=my_dbm.pets
    cat1 = pet("sniffles", 5, 25)
    cat2 = pet("fluff", 2, 15)

    #check if theres any pets there, dont add em
    #double inserts are bad mkay. maybe there should
    #be a check on insert for something with that ID
    if(len(list(pets.find()))==0):
        my_dbm.insert(my_dbm.pets,cat1)
        my_dbm.insert(my_dbm.pets,cat2)
        print("adding sniffles and fluff")

    print("sniffles entry: " + str(my_dbm.get_by_name(my_dbm.pets, "sniffles")))
    print("sniffles id:" + str(cat1.db_id))
    cat1.weight = 20

    my_dbm.replace(my_dbm.pets, cat1)
    print("updated sniffles")
    print(my_dbm.get_by_name(my_dbm.pets, "sniffles"))




main()
