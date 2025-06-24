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

    def takeAction(self):
        try:
            print(self.actions["melee attack"](self.battelfield.allCreatures))
            return True
        except ValueError:
            pass
        try:
            print(self.actions["ranged attack"](self.battelfield.allCreatures))
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






