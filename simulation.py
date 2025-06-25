from Battelfield import Battelfield
from Monster import Monster
from Character import Character
from copy import deepcopy

class simulation():
    def __init__(self, gobNum:int, wizard:bool, fighter:bool, paladin:bool):
        self.monsters = []
        self.characters = []
        self.board = None
        for x in range(1, gobNum+1):
            goblin = Monster(str(x)+"Goblin", 7, 15, 9, self, -1, 2, 0, 0, -1, -1, "Goblinoid", 2, 30, {"Stealth": +6}, 1,6, 80, 6, 4)
            goblin.addBonusAction("disengage", goblin.actions["disengage"])
            goblin.addAction("hide", goblin.actions["hide"])
            goblin.setYX(1, x)
            self.monsters.append(goblin)
        if wizard:
            wizard = Character("Wizard", 7, 10, 11, None, -1, 1, 1, 3, 1, -1, "wizard", 1)
            wizard.setYX(5, 5)
            self.characters.append(wizard)
        if fighter:
            fighter = Character("Fighter", 13, 10, 10, None, 3, 3, 3, -1, 0, 0, "fighter", 1)
            fighter.setYX(5, 6)
            self.characters.append(fighter)
        if paladin:
            paladin = Character("Paladin", 13, 10, 10, None, 3, 1, 3, -2, 0, 3, "paladin", 1)
            paladin.setYX(6, 5)
            self.characters.append(paladin)



    def createBattelfield(self, testNumber:int, size:int):
       return Battelfield(testNumber, size)

    def addCreature(self, board:Battelfield, creautre, y, x):
        board.addCreature(creautre, y, x)

    def setBoard(self, testNumber:int, size:int):
        board = self.createBattelfield(testNumber, size)
        board.printBattelfield()
        for mon in self.monsters:
            monY, monX = mon.getYX()
            mon.battelfield = board
            board.addCreature(mon, monY, monX)

        for char in self.characters:
            charY, charX = char.getYX()
            char.battelfield = board
            board.addCreature(char, charY, charX)
        return board

    def sample(self, board:Battelfield):
        counter = 0
        board.rollInitive()
        board.resetMoves()
        while board.winCondision() == 2:
            counter += 1
            board.nextTurn()[1].MCTS(100)
            print("counter of turns:" + str(counter))

        if board.winCondision() == 0:
            return True
        if board.winCondision() == 1:
            return False




test = simulation(3, True, True, True)

control = test.setBoard(1, 8)
control.printBattelfield()

wins = 0
for x in range(1, 100):
    if test.sample(deepcopy(control)):
        wins += 1
    print(wins)

print(wins)

#control.printBattelfield()
