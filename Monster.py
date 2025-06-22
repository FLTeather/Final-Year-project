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

    def meleeAttack(self, target, addvantage=False, disadvantage=False):
        if target.AC <= self.rollD20(addvantage=addvantage, disadvantage=disadvantage)+self.attackMod:
            target.takeDamage(self.rollDX(self.meleeDam)+self.attackMod-self.profMod)
            return "hits"
        return "misses"

    def rangedAttack(self, target, addvantage=False, disadvantage=False):
        if target.AC <= self.rollD20(addvantage=addvantage, disadvantage=disadvantage)+self.attackMod:
            target.takeDamage(self.rollDX(self.meleeDam)+self.attackMod-self.profMod)
            return "hits"
        return "misses"






