from random import randint
class Creature:
    def __init__(self, name, HP, AC, passPerc, battelfield, stre, dex):
        self.name = name
        self.HP = HP
        self.AC = AC
        self.passivePercetion = passPerc
        self.actions = ["disengage", "dash", "hide", "help", "meleeAttack"]
        self.bonusActions = []
        self.speed = 6 # Speed as in number of 5ft squares not as in 6ft.
        self.roundspeed = 0
        self.y = 0
        self.x = 0
        self.disengaged = False
        self.isHidden = False
        self.battelfield = battelfield
        self.strength = stre
        self.dexterity = dex
        self.profMod = 2
        self.hasAdvantage = False # If you have advantage on attacks
        self.isAdvantage = False #If someone has advantage to hit you
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
        self.HP += damage

    def dash(self):
        return self.speed * 2

    def hide(self, dc):
        if self.battelfield.canHide(self):
            if self.rollD20()+self.dexterity >= dc:
                self.isHidden = True
        else:
            self.isHidden = False
    def search(self, dc):
        if dc > self.rollD20():
            self.isHidden = False

    def disengage(self):
        self.disengaged = True

    def meleeAttack(self, target, addvantage=False, disadvantage=False):
        if target.ac <= self.rollD20(addvantage=addvantage, disadvantage=disadvantage)+4:
            target.takeDamage(self.rollDX(4))

    def oppetuinityAttack(self, target):
        if self.canReact:
            maxStat = max(self.strength, self.dexterity)
            self.meleeAttack(self.rollDX(4), maxStat+self.profMod, target, addvantage=self.isHidden or self.hasAdvantage or target.isAdvantage, disadvantage=target.isHidden)
        self.canReact = False

    def help(self, creature):
        creature.isAdvantage = True



