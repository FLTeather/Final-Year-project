from Character import *
# This class will handle the turn choice which is why it looks so empty right now.

class PLayerController:
    def __init__(self):
        self.monsters = []

    def takeTurn(self, monster):
        character.takeTurn()