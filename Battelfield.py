from Squares import Squares
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
        self.battelfield = [[Squares() for y in range(self.size)] for x in range(self.size)]

        for y in range(self.size):
            for x in range(self.size):
                if y == 0 or y == self.size-1 or x == 0 or x == self.size-1:
                    self.battelfield[y][x].isWall = True


    def printBattelfield(self):
        for rows in self.battelfield:
            print(rows)
    def addCreature(self, creature):
        self.allCreatures.append(creature)

    def removeCreature(self, creature):
        self.allCreatures.remove(creature)
