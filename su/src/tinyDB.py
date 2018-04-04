import btree
from gc import collect, mem_free

dbname="tiny.db"
key=b"key"
calib=b"calib"
wb="w+b"

def __write__(k,val):
    collect()
    file = open(dbname,wb)
    db = btree.open(file)
    db[k] = val 
    __clean__(db,file)

def __clean__(d,f):
    d.flush()
    d.close()
    f.close()
    collect()

class TinyDB:
    def __init__(self):
        try:
            file = open(dbname, "r+b")
            db = btree.open(file)
            self.key = db[key]
            self.calib = db[calib]
            __clean__(db,file)

        except OSError:
            file = open(dbname, wb)
            db = btree.open(file)
            self.key = ""
            self.calib = ""
            db[key] = self.key
            db[calib] = self.calib
            __clean__(db,file)

    def getKey(self):
        return self.key

    def setKey(self, val):
        self.key = val
        __write__(key,val)

    def getCalib(self):
        return self.calib

    def setCalib(self, val):
        self.calib=val
        __write__(calib,val)
