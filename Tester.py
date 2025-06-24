from Battelfield import Battelfield
from Monster import Monster
from Character import Character


battelfield = Battelfield(1, 15)
battelfield.printBattelfield()




goblin1 = Monster("1Goblin", 7, 15, 9, battelfield, -1, 2, 0, 0, -1, -1, "Goblinoid", 2, 30, {"Stealth":+6}, 1, 6, 80, 6, 4)
goblin1.addBonusAction("disengage", goblin1.actions["disengage"])
goblin1.addAction("hide", goblin1.actions["hide"])

goblin2 = Monster("2Goblin", 7, 15, 9, battelfield, -1, 2, 0, 0, -1, -1, "Goblinoid", 2, 30, {"Stealth":+6}, 1, 6, 80, 6, 4)
goblin2.addBonusAction("disengage", goblin2.actions["disengage"])
goblin2.addAction("hide", goblin2.actions["hide"])

goblin3 = Monster("3Goblin", 7, 15, 9, battelfield, -1, 2, 0, 0, -1, -1, "Goblinoid", 2, 30, {"Stealth":+6}, 1, 6, 80, 6, 4)
goblin3.addBonusAction("disengage", goblin3.actions["disengage"])
goblin3.addAction("hide", goblin3.actions["hide"])

goblin4 = Monster("4Goblin", 7, 15, 9, battelfield, -1, 2, 0, 0, -1, -1, "Goblinoid", 2, 30, {"Stealth":+6}, 1, 6, 80, 6, 4)
goblin4.addBonusAction("disengage", goblin4.actions["disengage"])
goblin4.addAction("hide", goblin4.actions["hide"])


battelfield.addCreature(goblin1, 2, 2)
battelfield.addCreature(goblin2, 2, 3)
battelfield.addCreature(goblin3, 3, 2)
battelfield.addCreature(goblin4, 3, 3)


wizard = Character("Jeff", 7, 10, 11, battelfield, -1, 1, 1, 3, 1, -1, "wizard", 1)
battelfield.addCreature(wizard, 13, 13)

paladin = Character("Lucy", 13, 10, 10, battelfield, 3, 1, 3, -2, 0, 3, "paladin", 1)
battelfield.addCreature(paladin, 12, 13)

Fighter = Character("Cath", 13, 10, 10, battelfield, 3, 3, 3, -1, 0, 0, "fighter", 1)
battelfield.addCreature(Fighter, 13, 12)

battelfield.printBattelfield()

battelfield.rollInitive()

battelfield.resetMoves()

counter = 0

while battelfield.winCondision() == 2:
    print(battelfield.winCondision())
    counter += 1
    battelfield.nextTurn()[1].takeTurn()
    battelfield.printBattelfield()
    print(counter)

print(battelfield.winCondision())

