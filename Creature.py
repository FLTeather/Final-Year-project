from random import randint
class Creature:
    def __init__(self, name, HP, AC, passPerc, battelfield, stre, dex):
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
        self.strength = stre
        self.dexterity = dex
        self.profMod = 2
        self.hasAdvantage = False
        self.canReact = True # True when can be used


    def setXY(self, y, x):
        self.y = y
        self.x = x

    def getXY(self):
        return self.y, self.x

    def rollD20(self, addvantage=False, disadvantage=False):
        if addvantage and disadvantage:
            pass
        if addvantage:
            return max(randint(1, 20), randint(1, 20))
        if disadvantage:
            return min(randint(1, 20), randint(1, 20))

        return randint(1, 20)


    def rollDX(self, x):
        return randint(1, x)

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

    def attack(self, damage, attackMod, target, addvantage=False, disadvantage=False):
        if target.ac > self.rollD20()+attackMod:
            target.takeDamage(damage, addvantage, disadvantage)

    def oppetuinityAttack(self, target):
        if self.canReact:
            maxStat = max(self.strength, self.dexterity)
            self.attack(self.rollDX(4), maxStat+self.profMod, target, addvantage=self.isHidden or self.hasAdvantage, disadvantage=target.isHidden)
        self.canReact = False




