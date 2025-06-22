from random import randint, choice, shuffle

class Creature:
    def __init__(self, name, HP, AC, passPerc, battelfield, stre, dex):
        self.controller = None
        self.name = name
        self.HP = HP
        self.maxHP = HP
        self.AC = AC
        self.passivePercetion = passPerc
        self.actions = {"disengage": self.disengage, "dash": self.dash, "hide" :self.hide, "help":self.help, "meleeAttack":self.meleeAttack}
        self.bonusActions = {}
        self.speed = 6 # Speed as in number of 5ft squares not as in 6ft.
        self.turnSpeed = self.speed
        self.roundspeed = 0
        self.y = 0
        self.x = 0
        self.disengaged = False
        self.isHidden = False # False when not hidden
        self.isDodged = False
        self.battelfield = battelfield
        self.strength = stre
        self.dexterity = dex
        self.wizdom = 2
        self.profMod = 2
        self.hasAdvantage = False # If you have advantage on attacks
        self.isAdvantage = False #If someone has advantage to hit you
        self.canReact = True # True when can be used
        self.abilityTracking = {}  # ability name : usesleft
        self.allMoves = []
        self.isdead = False

    def takeTrun(self):
        choices = ["move", "action", "bonus"]
        if len(self.bonusActions) == 0:
            choices.remove("bonus")
        while len(choices) != 0 and not self.isdead:
            selection = choice(choices)
            if selection == "move":
                square = choice(self.getAllAdjecentMoves())
                self.move(square[0], square[1])
                self.turnSpeed -= 1
                print("I moved: ", self.turnSpeed)
                if self.turnSpeed < 0:
                    choices.remove("move")
            elif selection == "action":
                if self.takeAction():
                    choices.remove("action")

            elif selection == "bonus":
                key = choice([key for key in self.bonusActions])
                try:
                    self.bonusActions[key](self.battelfield.dealDamage)
                    choices.remove("bonus")
                except ValueError:
                    pass
            if self.isdead:
                self.battelfield.removeCreature(self)
            self.battelfield.printBattelfield()



    def takeAction(self):
        key = choice([key for key in self.actions])
        try:
            shuffle(self.battelfield.allCreatures)
        except ValueError:
            return False
        return True


    def setYX(self, y, x):
        self.y = y
        self.x = x

    def getYX(self):
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

    #damage should be passed as a postive value, healing as a negative
    def takeDamage(self, damage):
        self.HP -= damage
        if self.HP <= 0:
            print(self.name, " has died")
            self.isdead = True

    def dash(self, targets):
        self.turnSpeed += self.speed
        return "dashsed"

    def hide(self, targets):
        if self.battelfield.canHide(self):
            if self.rollD20()+self.dexterity >= self.battelfield.highPP():
                self.isHidden = True
                return "Hidden"
        else:
            self.isHidden = False
            return "Failed Hidden"
    def search(self, targets):
        self.battelfield.saerch(self, self.rollD20()+self.wizdom)
        return "Searched"

    def disengage(self, targets):
        self.disengaged = True
        return "disengaged"

    def meleeAttack(self, targets, addvantage=False, disadvantage=False):
        output = "melee attack: \n"
        from Monster import Monster
        target = self.pickAjecentTarget(targets, Monster)
        if target.AC <= self.rollD20(addvantage=addvantage, disadvantage=disadvantage)+self.strength+self.profMod:
            output += "\thits" + target.name +"\n"
            target.takeDamage(self.rollDX(4)+self.strength)
        return output

    def oppetuinityAttack(self, target, y, x):
        output = "oppetunity Attack:\n"
        if not self.canReact:
            output += "\t" + self.name +"no reaction\n"
            return output

        if (y, x) not in self.getAllAdjcentSqaure():
            output += "\t" + self.name +" not valid attack\n"
            return output

        self.canReact = False
        addvantage = bool(self.isHidden or self.hasAdvantage or target.isAdvantage)
        disadvantage = target.isHidden
        output += self.meleeAttack(target, addvantage=addvantage, disadvantage=disadvantage)
        return output

    def help(self, targets):
        from Monster import Monster
        target = self.pickAjecentTarget(targets, Monster)
        target.isAdvantage = True

    def addBonusAction(self, key, action):
        self.bonusActions.update({key:action})

    def addAction(self, key, action):
        self.actions.update({key:action})

    def dodge(self, targets):
        self.isDodged = True

    def __repr__(self):
        return self.name

    def getAllAdjcentSqaure(self):
        y, x = self.getYX()
        moves = []
        for move in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            possibleMove = (y + move[0], x + move[1])
            moves.append(possibleMove)

        return moves

    def getAllAdjecentMoves(self):
        y, x = self.getYX()
        moves = []
        for move in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            possibleMove = (y + move[0], x + move[1])
            if possibleMove in self.allMoves:
                moves.append(possibleMove)

        return moves

    def move(self, y, x):
        self.battelfield.moveCreature(self, y, x)

    def pickSingleTarget(self, targets, creatureType):
        n = 0
        target = targets[n]
        while type(target) == creatureType:
            if n > len(targets)-1:
                raise ValueError("No valid Target")
            n = n+1
            target = targets[n]

        return target

    def pickAjecentTarget(self, targets, creatureType):
        newTargets = []
        for target in targets:
            targetY, targetX = target.getYX()
            if targetY-self.y > 1 or targetY-self.y < -1:
                continue
            if targetX-self.x > 1 or targetX-self.x < -1:
                continue
            newTargets.append(target)
        if len(newTargets) == 0:
            raise ValueError("No valid Target")
        return self.pickSingleTarget(newTargets, creatureType)





