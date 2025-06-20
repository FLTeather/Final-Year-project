# This class will handle the turn choice which is why it looks so empty right now.

class MonsterController:
    def __init__(self, battelfeild):
        self.monsters = []
        self.battelfeild = battelfeild

    def addMonster(self, monster):
        self.monsters.append(monster)
        monster.monsterController = self

    def takeTurn(self, monster):
        print(monster.actions)