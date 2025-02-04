from Battelfield import Battelfield
class simulation():
    def __init__(self, name, size):
        self.name = name
        battelfield = Battelfield(1, size)
        battelfield.printBattelfield()


simulation("test", 10)

