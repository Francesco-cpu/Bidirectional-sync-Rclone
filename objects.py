class MyFile:
    def __init__(self,path, size, lastModificationDate):
        self.name=path 
        self.size = size
        self.lastModificationDate = lastModificationDate
    def __str__(self):
        return self.name + " " + str(self.size) + " " + str(self.lastModificationDate.timestamp())
    def __repr__(self):
        return self.name + " " + str(self.size) + " " + str(self.lastModificationDate)
    def __eq__(self, other):
        return self.name == other.name and self.size == other.size and self.lastModificationDate == other.lastModificationDate
    def __hash__(self):
        return hash((self.name, self.size, self.lastModificationDate))