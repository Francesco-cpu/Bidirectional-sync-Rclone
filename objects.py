class MyFile:
    def __init__(self,path, size, lastModificationDate):
        self.name=path 
        self.size = size
        self.lastModificationDate = lastModificationDate
    def __str__(self):
        return self.name + " " + str(self.size) + " " + str(self.lastModificationDate.timestamp())
    def __repr__(self):
        return self.name + " " + str(self.size) + " " + str(self.lastModificationDate)
    