class Creature:
    def __init__(self, name, HP, AC, passPerc, battelfield):
        self.name = name
        self.HP = HP
        self.AC = AC
        self.passivePercetion = passPerc
        self.actions = []
        self.bonusActions = []
        self.speed = 6 # Speed as in number of 5ft squares not as in 6ft.
        self.y = 0
        self.x = 0
        self.allMoves = []
        self.disengaged = False
        self.isHidden = False
        self.battelfield = battelfield

    def setXY(self, y, x):
        self.y = y
        self.x = x

    def getXY(self):
        return self.y, self.x

    def setAllMoves(self, allMoves):
        self.allMoves = allMoves

    #damage should be passed as a negative value, healing as a postive
    def takeDamage(self, damage):
        self.hp += damage

    def dash(self):
        return self.speed * 2

    def hide(self):
        if self.battelfield.canHide(self):
            self.isHidden = True
        else:
            self.isHidden = False