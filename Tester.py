from Battelfield import Battelfield
from copy import deepcopy
from MonsterController import MonsterController
from PlayerController import PlayerController
from Monster import Monster
from Character import Character


battelfield = Battelfield(1, 15)
battelfield.printBattelfield()


goblin = Monster("Goblin", 7, 15, 9, battelfield, -1, 2, 0, 0, -1, -1, "Goblinoid", 2, 30, {"Stealth":+6}, 1, 6, 80, 6, 4)

goblin.addBonusAction("disengage", goblin.actions["disengage"])
goblin.addAction("hide", goblin.actions["hide"])

goblin1 = deepcopy(goblin)
goblin1.name = "1Goblin"
goblin2 = deepcopy(goblin)
goblin2.name = "2Goblin"
goblin3 = deepcopy(goblin)
goblin3.name = "3Goblin"
goblin4 = deepcopy(goblin)
goblin4.name = "4Goblin"

battelfield.addCreature(goblin1, 10, 10)
battelfield.addCreature(goblin2, 10, 11)
battelfield.addCreature(goblin3, 11, 10)
battelfield.addCreature(goblin4, 11, 11)


wizard = Character("Jeff", 7, 10, 11, battelfield, -1, 1, 1, 3, 1, -1, "wizard", 1)
battelfield.addCreature(wizard, 13, 13)

paladin = Character("Lucy", 13, 10, 10, battelfield, 3, 1, 3, -2, 0, 3, "paladin", 1)
battelfield.addCreature(paladin, 12, 13)

Fighter = Character("Cath", 13, 10, 10, battelfield, 3, 3, 3, -1, 0, 0, "fighter", 1)
battelfield.addCreature(Fighter, 13, 12)

battelfield.printBattelfield()

battelfield.rollInitive()

battelfield.resetMoves()
goblin1.takeTrun()
wizard.takeTrun()
paladin.takeTrun()
Fighter.takeTrun()
print(battelfield.allCreatures)
if goblin1 in battelfield.allCreatures:
    print("YES")
else:
    print("NO")


