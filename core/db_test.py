#testing functions to db shiz

from database_manager import dbm
from pet import pet

def main():
    my_dbm = dbm()
    cat1 = pet("sniffles", 5, 25)
    cat2 = pet("fluff", 2, 15)

    print("adding sniffles and fluff")

    my_dbm.insert(my_dbm.pets,cat1)
    my_dbm.insert(my_dbm.pets,cat2)

    print(my_dbm.get_by_name(my_dbm.pets, "sniffles"))
    #print(cat1.db_id)
    cat1.weight = 20

   # my_dbm.replace(my_dbm.pets, cat1)
    #print("updated sniffles")
    #print(my_dbm.get_by_name(my_dbm.pets, "sniffles"))




main()
