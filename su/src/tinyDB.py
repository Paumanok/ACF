import btree


class TinyDB:
    def __init__(self):
        try:
            self.file = open("tiny.db", "r+b")
            self.db = btree.open(self.file)
        except OSError:
            self.file = open("tiny.db", "w+b")
            self.db = btree.open(self.file)
            self.db[b"key"] = ""

    def getKey(self):
        return self.db[b"key"]

    def setKey(self, key):
        self.db[b"key"] = key
        self.db.flush()

    def getCalib(self):
        return self.db[b"calib"]

    def setCalib(self, calib):
        self.db[b"calib"] = calib
        self.db.flush()
