class Artist:
    def __init__(self,name,id):
        self.name = name
        self.id = id

    def __str__(self):
        return self.name + ' | ' + self.id
