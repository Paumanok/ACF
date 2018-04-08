import gc

dbname="tiny.db"
wb="w+b"
rb="r+b"
split=b':'

def __read__():
    file = open(dbname, rb)
    vals = file.read().split(b':')
    file.close()
    gc.collect()
    return vals

def __write__(v):
    file = open(dbname, wb)
    file.write(split.join(v))
    file.close()
    gc.collect()

class TinyDB:
    def __init__(self):
        try:
            self.vals = __read__()

        except OSError:
            file = open(dbname, wb)
            self.vals = [b'0',b'0']
            file.write(b'0:0')
            file.close()
            gc.collect()

    def getKey(self):
        return self.vals[0]

    def setKey(self, val):
        self.vals[0] = val
        __write__(self.vals)

    def getCalib(self):
        return self.vals[1]

    def setCalib(self, val):
        self.vals[1]=val
        __write__(self.vals)
