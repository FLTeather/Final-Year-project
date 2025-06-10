from Battelfield import Battelfield
from Creature import Creature
class simulation():
    def __init__(self, name, size):
        self.name = name
        self.battelfield = Battelfield(1, size)
        self.battelfield.printBattelfield()
        self.creatures = []

    def addCreature(self, name, hp, ac, y, x):
        creature = Creature(name, hp, ac)
        self.battelfield.addCreature(creature, y, x)
        self.creatures.append(creature)
        self.battelfield.printBattelfield()

    def random(self):
        self.addCreature("John", 2, 10, 2, 4)
        #print(self.battelfield.getAllPossibleMoves( 2, 2, 6))
        #print(self.battelfield.moveCreature(self.creatures[0], 4, 4))
        #self.battelfield.printBattelfield()


    def line(self, creature1, creature2):
        print(self.battelfield.canSee(creature1, creature2))


sim = simulation("test", 20)
sim.addCreature("Dave",  1, 10, 2, 2)
sim.random()

sim.battelfield.battelfield[2][3].isWall = True
sim.battelfield.printBattelfield()

sim.line(sim.creatures[0], sim.creatures[1])
