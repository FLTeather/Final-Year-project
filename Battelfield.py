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
        print("\n\n")
    def addCreature(self, creature, y, x):
        self.allCreatures.append(creature)
        self.battelfield[y][x].creature = creature
        self.battelfield[creature.y][creature.x].isDifficultTerrain = True
        creature.setXY(y, x)
        creature.setAllMoves(self.getAllPossibleMoves(y, x, creature.speed))

    def removeCreature(self, creature):
        self.battelfield[creature.y][creature.x].creature = None
        self.battelfield[creature.y][creature.x].isDifficultTerrain = False
        self.allCreatures.remove(creature)

    def getAllPossibleMoves(self, y, x, speed):
        allNodes = {}
        visitedNodes = {}
        possibleMoves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        for a in range(self.size):
            for b in range(self.size):
                if self.battelfield[a][b].isWall:
                    continue
                allNodes.update({(a, b): speed+1})
        allNodes.update({(y, x): 0})

        while len(allNodes) != 0:
            minValue = min(allNodes, key=allNodes.get)
            currentDistance = allNodes[minValue]
            if currentDistance > speed:
                break
            for move in possibleMoves:
                try:
                    checkDistance = allNodes[(minValue[0]+move[0], minValue[1]+move[1])]
                    if checkDistance > currentDistance:
                        if self.battelfield[minValue[0]+move[0]][minValue[1]+move[1]].isDifficultTerrain:
                            allNodes.update({(minValue[0] + move[0], minValue[1] + move[1]): currentDistance + 2})
                        else:
                            allNodes.update({(minValue[0] + move[0], minValue[1] + move[1]): currentDistance + 1})

                except KeyError as e:
                    pass # The lack of Key implies the squear is a wall
            visitedNodes.update({minValue:currentDistance})
            allNodes.pop(minValue)
        outputNodes = [keys for keys in visitedNodes if self.battelfield[keys[0]][keys[1]].creature is None]
        return outputNodes


    def canMove(self, creature, y, x):
        if (y, x) in creature.allMoves:
            return True
        return False

    def moveCreature(self, creature, y, x):
        if not self.canMove(creature, y, x):
            return False
        self.removeCreature(creature)
        self.addCreature(creature, y, x)

        return True

    def dealDamage(self, y, x, damage):
        if self.battelfield[y][x].creature is None:
            pass
        else:
            self.battelfield[y][x].creature.takeDamage(damage)