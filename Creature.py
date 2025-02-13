class Creature:
    def __init__(self, name, HP, AC):
        self.name = name
        self.HP = HP
        self.AC = AC
        self.actions = []
        self.speed = 6 # Speed as in number of 5ft squeres not as in 6ft.
        self.y = 0
        self.x = 0

    def setXY(self, y, x):
        self.y = y
        self.x = x
