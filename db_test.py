#testing functions to db shiz

from core.database_manager import dbm
from core.db_types.pet import pet

def main():
    my_dbm = dbm()
    pets=my_dbm.pets
    cat1 = pet("sniffles", 5, 25)
    cat2 = pet("fluff", 2, 15)

    print("does sniffles exist before? " + str(len(list(pets.find({"name":"sniffles"})))))
    my_dbm.insert(my_dbm.pets,cat1)
    my_dbm.insert(my_dbm.pets,cat2)
    print("adding sniffles and fluff")
    print("does sniffles exist after? " + str(len(list(pets.find({"name":"sniffles"})))))

    print("sniffles entry: " + str(my_dbm.get_by_name(my_dbm.pets, "sniffles")))
    print("sniffles id:" + str(cat1.db_id))
    cat1.weight = 20

    my_dbm.replace(my_dbm.pets, cat1)
    print("updated sniffles")
    print(my_dbm.get_by_name(my_dbm.pets, "sniffles"))




main()
