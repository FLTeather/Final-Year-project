from Monster import Monster
from Squares import Squares

class Battelfield:
    def __init__(self, tn, size):
        self.testNumber = tn
        self.size = size # Size both X and Y
        self.allCreatures = []
        self.battelfield = []
        self.setUpBattelfield()
        self.initiativeOrder = []
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
        if self.battelfield[y][x].creature != None:
            raise ("Another creature already in space")
        self.battelfield[y][x].creature = creature
        self.battelfield[y][x].isDifficultTerrain = True
        creature.setYX(y, x)
        creature.setAllMoves(self.getAllPossibleMoves(y, x, creature.speed))
        self.resetMoves()

    def removeCreature(self, creature):
        self.battelfield[creature.y][creature.x].creature = None
        self.battelfield[creature.y][creature.x].isDifficultTerrain = False
        self.allCreatures.remove(creature)

    def getAllPossibleMoves(self, y, x, speed):
        allNodes = {}
        visitedNodes = {}
        possibleMoves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
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
        if not creature.disengaged:
            self.opponentAttack(creature)
        self.removeCreature(creature)
        self.addCreature(creature, y, x)
        return True

    def opponentAttack(self, creature):
        oldY, oldX = creature.getYX()
        possibleDirections = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for direction in possibleDirections:
            creatureDirection = self.battelfield[oldY - direction[0]][oldX - direction[1]].creature
            if creatureDirection is not None and type(creatureDirection) != type(creature):
                creatureDirection.oppetuinityAttack(creature, oldY, oldX)
        return True
    def dealDamage(self, y, x, damage):
        if self.battelfield[y][x].creature is None:
            pass
        else:
            self.battelfield[y][x].creature.takeDamage(damage)

    def dealDexSaveDamage(self, y, x, damage):
        if self.battelfield[y][x].creature is None:
            pass
        else:
            if self.battelfield[y][x].creature.rollD20()+self.battelfield[y][x].creature.dexterity:
                self.battelfield[y][x].creature.takeDamage(damage)
            else:
                self.battelfield[y][x].creature.takeDamage(damage//2)

    # given two creatures, returns all squares between creatures
    def lineOfSight(self, creature0, creature1):
        points = []
        y0, x0 = creature0.getYX()
        y1, x1 = creature1.getYX()

        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            x0, y0 = y0, x0
            y1, x1 = y1, x1
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = x1 - x0
        dy = abs(y1 - y0)
        error = 0
        yStep = -1
        y = y0
        if y0 < y1:
            yStep = 1

        for x in range(x0, x1+1):
            if steep:
                points.append((x, y))
            else:
                points.append((y, x))

            error += dy
            if error >= dx:
                y += yStep
                error -= dx
        return points

    def canSee(self, creature0, creature1):
        points = self.lineOfSight(creature0, creature1)
        for point in points:
            if self.battelfield[point[0]][point[1]].isWall:
                return False
        return True

    def canHide(self, creature):
        highPassivePerception = 0
        for creatures in self.allCreatures:
            # Creatures can hide if visible from teammates
            if type(creatures) == type(creature):
                continue
            if creatures.passivePercetion > highPassivePerception:
                highPassivePerception = creatures.passivePercetion
            # can see returns true when creatures can see
            if self.canSee(creatures, creature):
                return False

    def allSeenCreatures(self, creature, ranged=0):
        return [creatures for creatures in self.allCreatures if self.canSee(creatures, creature)]

    def rollInitive(self):
        for creatures in self.allCreatures:
            inti = creatures.rollD20()+creatures.dexterity
            self.initiativeOrder.append([inti, creatures])

        self.sortCreatures()
        print(self.initiativeOrder)

    def sortCreatures(self):
        self.initiativeOrder.sort(
            key=lambda x: (-x[0], -x[1].dexterity, x[1].name.lower())
        )
    def nextTurn(self):
        self.initiativeCount -= 1
        if self.initiativeCount < 0:
            self.initiativeCount = len(self.initiativeOrder)
            return self.nextTurn()
        return self.initiativeOrder[self.initiativeCount]

    def winCondision(self):
        monsters = [monsters for monsters in self.allCreatures if type(monsters) == Monster]
        players = [chars for chars in self.allCreatures if type(chars) != Monster]
        if len(monsters) == 0:
            return 0
        elif len(players) == 0:
            return 1
        else:
            return 2


    def resetMoves(self):
        for creature in self.allCreatures:
            y, x = creature.getYX()
            creature.setAllMoves(self.getAllPossibleMoves(y, x, creature.speed))

    def highPP(self, creature):
        highestPP = 0
        for creatures in self.allCreatures:
            if type(creatures) == type(creature):
                continue
            if creatures.passivePercetion > highestPP:
                highestPP = creatures.passivePercetion

        return highestPP

    def saerch(self, creature, dc):
        for creatures in self.allCreatures:
            if not creatures.isHidden:
                continue
            if not self.canHide(creatures, creature):
                pass

            if creatures.rollD20() > dc:
                creatures.isHidden = False
    def creatureDied(self, deadCreature):
        self.removeCreature(deadCreature)
        for inatives in self.initiativeOrder:
            if inatives[1] == deadCreature:
                self.initiativeOrder.remove(inatives)
        self.initiativeCount -=1


