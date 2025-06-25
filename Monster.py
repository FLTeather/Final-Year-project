from Creature import Creature


class Monster(Creature):
    def __init__(self, name, HP, AC, passPerc, battelfield, stre, dex, con, inte, wiz, char, type, profBonus, speed, skills, meleeRange, meleeDam, rangedRange, rangedDam, attackMod):
        Creature.__init__(self, name, HP, AC, passPerc, battelfield, stre, dex)
        self.type = type
        self.profMod = profBonus
        self.speed = speed/5
        self.wizdom = wiz
        self.charisma = char
        self.inteligence = inte
        self.consitution = con
        self.skills = skills #format dic {skill:mod}
        self.meleeRange = meleeRange
        self.meleeDam = meleeDam
        self.rangedRange = rangedRange
        self.rangedDam = rangedDam
        self.attackMod = attackMod
        self.actions.update({"ranged attack": self.rangedAttack})

    def MCTS(self, samNum):
        if self.isdead:
            return

        from MonteCarloTreeSearch import MonteCarloTreeSearch
        mtcs = MonteCarloTreeSearch(self.battelfield, isMonster=True)

        while mtcs.n() < samNum:
            # print("Counter of creature turn checks"+ str(mtcs.n()))
            mtcs.selection()
        bestMove = mtcs.best_child().lastMove
        print(self.name)
        print(self.turnSpeed)
        print(bestMove)
        if bestMove[0] == "action":
            self.actions[bestMove[1]](self.battelfield.allCreatures)
            self.choices.remove(bestMove[0])
        elif bestMove[0] == "bonus":
            self.bonusActions[bestMove[1]](self.battelfield.allCreatures)
            self.choices.remove(bestMove[0])
        elif bestMove[0] == "move":
            self.move(bestMove[1][0], bestMove[1][1])
            self.turnSpeed -= 1

        if self.choices == [] or bestMove[0] == None:
            # Turn ended
            self.choices = ["action", "move"]
            self.turnSpeed = self.speed
            if len(self.bonusActions) != 0:
                self.choices.append("bonus")
            return

        self.battelfield.printBattelfield()
        self.MCTS(samNum)

    def takeAction(self):
        try:
            self.actions["melee attack"](self.battelfield.allCreatures)
            return True
        except ValueError:
            pass
        try:
            self.actions["ranged attack"](self.battelfield.allCreatures)
        except ValueError:
            return False
        return True

    def pickSingleTarget(self, targets, creatureType):
        n = 0
        target = targets[n]
        while type(target) != creatureType:
            n = n + 1
            if n > len(targets)-1:
                raise ValueError("No valid Target")
            target = targets[n]
            if target.klass == "wizard":
                return target

        return target
    def meleeAttack(self, targets, addvantage=False, disadvantage=False):
        from Character import Character
        target = self.pickAjecentTarget(targets, Character)
        if target.AC <= self.rollD20(addvantage=addvantage, disadvantage=disadvantage)+self.attackMod:
            target.takeDamage(self.rollDX(self.meleeDam)+self.attackMod-self.profMod)
            return "hits " + target.name
        return "misses "+ target.name

    def rangedAttack(self, targets, addvantage=False, disadvantage=False):
        from Character import Character
        target = self.pickSingleTarget(targets, Character)
        if target.AC <= self.rollD20(addvantage=addvantage, disadvantage=disadvantage)+self.attackMod:
            target.takeDamage(self.rollDX(self.meleeDam)+self.attackMod-self.profMod)
            return "hits " + target.name
        return "misses "+ target.name






