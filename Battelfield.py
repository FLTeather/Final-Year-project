class Battelfield:
    def __init__(self, tn, size):
        self.testNumber = tn
        self.size = size # Size both X and Y
        self.allCreatures = []
        self.battelfield = []
        self.setUpBattelfield()
        self.initiativeOrder = {} # creature, initive number
        self.initiativeCount = 0

    def setUpBattelfield(self):
        self.battelfield = [["." for y in range(self.size)] for x in range(self.size)]

    def printBattelfield(self):
        for rows in self.battelfield:
            print(rows)