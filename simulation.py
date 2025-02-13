from Battelfield import Battelfield
from Creature import Creature
class simulation():
    def __init__(self, name, size):
        self.name = name
        self.battelfield = Battelfield(1, size)
        self.battelfield.printBattelfield()
        self.creatures = []

    def addCreature(self, name, hp, ac):
        dave = Creature(name, hp, ac)
        self.battelfield.addCreature(dave, 2, 2)
        self.creatures.append(dave)
        self.battelfield.printBattelfield()

    def random(self):
        print(self.battelfield.moveCreature(self.creatures[0], 4, 4))
        self.battelfield.printBattelfield()


sim = simulation("test", 20)
sim.addCreature("Dave",  1, 10)

sim.random()

