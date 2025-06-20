# This class will handle the turn choice which is why it looks so empty right now.

class PLayerController:
    def __init__(self, battelfield):
        self.character = []
        self.battlefield = battelfield

    def addMonster(self, character):
        self.character.append(character)
        character.monsterController = self