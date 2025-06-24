from Battelfield import Battelfield
from Monster import Monster
from Character import Character


battelfield = Battelfield(1, 15)
battelfield.printBattelfield()

battelfield.addGoblin("1goblin", 7, 2, 2)
battelfield.addGoblin("2goblin", 7, 3, 3)
battelfield.addGoblin("3goblin", 7, 4, 4)
battelfield.addGoblin("4goblin", 7, 5, 5)

battelfield.printBattelfield()

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

