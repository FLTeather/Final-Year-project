# This class will handle the turn choice which is why it looks so empty right now.

class MonsterController:
    def __init__(self):
        self.monsters = []

    def takeTurn(self, monster):
        monster.takeTurn()