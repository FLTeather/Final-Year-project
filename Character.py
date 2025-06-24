from Creature import Creature
from Monster import Monster
from random import choice, shuffle
class Character(Creature):
    def __init__(self, name, HP, AC, passPerc, battelfield, stre, dex, con, inte, wiz, char, klass, level):
        Creature.__init__(self, name, HP, AC, passPerc, battelfield, stre, dex)
        self.wizdom = wiz
        self.charisma = char
        self.inteligence = inte
        self.consitution = con
        self.meleeRange = 1
        self.meleeDam = 4
        self.rangedRange = 10
        self.rangedDam = 4

        self.level = level
        self.actions.update({"ranged attack": self.rangedAttack})
        self.klass = klass
        self.assignClass(klass, level)
        self.dying = False
        self.dyingTracker = [0, 0]

    def takeDamage(self, damage):
        if self.dying:
            if damage > 0:
                self.dyingTracker[1] += 2
                if self.dyingTracker[1] > 2:
                    self.hasDied()
        self.HP -= damage
        if self.HP <= 0:
            self.dying = True
            self.HP = 0

    def hasDied(self):
        print(self.name, " has died")
        self.isdead = True
        self.battelfield.creatureDied(self)

    def deathSaves(self):
        if self.dyingTracker[0] == 3:
            return "stable at 0 HP"

        roll = self.rollD20()
        if roll == 20:
            self.HP = 1
            self.dying = False
        elif roll > 10:
            self.dyingTracker[0] += 1
        else:
            self.dyingTracker[1] += 1

        if self.dyingTracker[1] > 3:
            self.hasDied()
        return str(roll)+ " : " + str(self.dyingTracker)


    def takeTurn(self):
        print(self.name + " is taking turn")
        if self.dying == True:
            if self.HP > 0:
                self.dying = False
            print(self.deathSaves())
            return False

        if self.klass == "paladin":
            print(self.paladinAction())

        elif self.klass == "fighter":
            print(self.fightAction())

        elif self.klass == "wizard":
            print(self.wizardAction())
        else:
            super().takeAction()

    def paladinAction(self):
        for moves in range(self.turnSpeed):
            try:
                self.pickAjecentTarget(self.battelfield.allCreatures, Monster)
                return self.meleeAttack(self.battelfield.allCreatures)
            except ValueError:
                pass

            if self.abilityTracking["layOnHands"]>0:
                allies = [creatures for creatures in self.battelfield.allCreatures if type(creatures) == type(self)]
                for allie in allies:
                    if allie.maxHP != allie.HP:
                        sqaures = allie.getAllAdjecentMoves()
                        if sqaures in self.allMoves:
                            self.move(sqaures[0][0], sqaures[0][1])
                            return self.layOnHands(allie)

            square = choice(self.getAllAdjecentMoves())
            self.move(square[0], square[1])
            self.turnSpeed -= 1
            print(self.name + " moved: ", self.getYX())

        return self.rangedAttack(self.battelfield.allCreatures)


    def fightAction(self):
        for moves in range(self.turnSpeed):
            if self.HP < self.maxHP-6 and self.abilityTracking["second wind"]>0:
                return self.secondWind(self.battelfield.allCreatures)

            try:
                self.pickAjecentTarget(self.battelfield.allCreatures, Monster)
                return self.meleeAttack(self.battelfield.allCreatures)
            except ValueError:
                pass

            square = choice(self.getAllAdjecentMoves())
            self.move(square[0], square[1])
            self.turnSpeed -= 1
            print(self.name + " moved: ", self.getYX())

        return self.rangedAttack(self.battelfield.allCreatures)


    def wizardAction(self):
        for moves in range(self.turnSpeed):
            try:
                self.pickAjecentTarget(self.battelfield.allCreatures, Monster)
                if not self.disengaged:
                    self.disengage(None)
            except ValueError:
                if self.abilityTracking["Level 1 spell slots"]>0:
                    if self.AC < 13 +self.dexterity:
                        return self.mageArmour(None)
                    if len ([creatures for creatures in self.battelfield.allCreatures if type(creatures) != type(self)]) >1:
                        return self.magicMissile(self.battelfield.allCreatures)
                    return self.chramaticOrb(self.battelfield.allCreatures)
                else:
                    return self.tollTheDead(self.battelfield.allCreatures)

            square = choice(self.getAllAdjecentMoves())
            self.move(square[0], square[1])
            self.turnSpeed -= 1
            print(self.name + " moved: ", self.getYX())
        return self.rangedAttack(self.battelfield.allCreatures)

    def assignClass(self, klass, level):
        self.classes = {"paladin": self.paladin, "wizard": self.wizard, "fighter": self.fighter}
        if klass in self.classes.keys():
            self.classes[klass.lower()](level)
        else:
            raise ValueError("Unknown class '{}'".format(klass))


    def paladin(self, level):
        self.AC = 16 # Chainmail
        self.meleeDam = 8 #Longsword
        self.AC += 2 #sheild
        self.rangedRange = 30 # Javelins
        self.rangedDam = 6
        self.abilityTracking.update({"divine sense": 1+self.charisma})
        self.actions.update({"divine sense": self.divineSense})
        self.abilityTracking.update({"layOnHands": level*5})
        self.actions.update({"layOnHands": self.layOnHands})


    def divineSense(self, targets):
        output = "Divine Sense:\n"
        if self.abilityTracking.get("divine sense") > 0:
            self.abilityTracking["divine sense"] -= 1
            for creatures in self.battelfield.allSeenCreatures(self, ranged=60):
                if creatures.type in ["celestial", "fiend", "undead"]:
                    creatures.isHidden = False
                    output += "\t"+ creatures.name + "was found" + "\n"
        else:
            raise ValueError("Divine sense less than 0")
        return output

    def layOnHands(self, targets):
        output = "Lay-On Hands:\n"
        target = self.pickAjecentTarget(targets, Character)
        targetY, targetX = target.getYX()
        amount = target.maxHP - target.HP
        if self.abilityTracking.get("layOnHands") >= amount:
            self.battelfield.dealDamage(targetY, targetX, amount*-1)
            self.abilityTracking["layOnHands"] -= amount
            output += "\t"+ target.name +"healed: " + str(amount) + "\n"
        else:
            raise ValueError("Lay-on hands less than {}".format(amount))
        return output

    def wizard (self, level):
        self.meleeDam = 6 #Quaterstaff

        self.actions.pop("ranged attack")
        # No need to add arcne recovery as it only applies outside of combat.
        self.abilityTracking.update({"Level 1 spell slots":2})
        self.actions.update({"firebolt": self.firebolt})
        self.actions.update({"tollTheDead": self.tollTheDead})
        # 6 level one spells are known but only two spell slots, let us assume that 2 of these spells that have no use in combat
        # Feather fall, detect magic and indentify
        self.actions.update({"magic missile": self.magicMissile})
        self.actions.update({"mage armour": self.mageArmour})
        self.actions.update({"chramatic orb": self.chramaticOrb})
    def mageArmour(self, targets):
        output = "Mage Armour:\n"
        if self.abilityTracking.get("Level 1 spell slots") >0:
            self.abilityTracking["Level 1 spell slots"] -= 1
            self.AC = 13 + self.dexterity
        else:
            raise ValueError("Level 1 spell slots less than 1")
        return output

    def magicMissile(self, targets):
        output = "Magic Missile:\n"
        target1 = self.pickSingleTarget(targets, Monster)
        shuffle(self.battelfield.allCreatures)
        target2 = self.pickSingleTarget(targets, Monster)
        shuffle(self.battelfield.allCreatures)
        target3 = self.pickSingleTarget(targets, Monster)
        if self.abilityTracking.get("Level 1 spell slots") >0:
            target1.takeDamage(self.rollDX(4)+1)
            if not target2.isdead:
                target2.takeDamage(self.rollDX(4)+1)
            if not target3.isdead:
                target3.takeDamage(self.rollDX(4)+1)
            self.abilityTracking["Level 1 spell slots"] -= 1
            output += "\t" + target1.name +"\n"
            output += "\t" + target2.name +"\n"
            output += "\t" + target3.name +"\n"
        else:
            raise ValueError("Level 1 spell slots less than 1")
        return output

    def chramaticOrb(self, targets):
        output = "Chramatic Orb:\n"
        if self.abilityTracking.get("Level 1 spell slots") >0:
            target = self.pickSingleTarget(targets, Monster)

            if target.AC > self.rollD20(addvantage=target.isAdvantage) + self.inteligence+self.profMod:
                target.takeDamage(self.rollDX(6)+self.rollDX(6)+self.rollDX(6))
                output += "\thits" + target.name +"\n"
            else:
                output += "\tmisses" + target.name +"\n"
            self.abilityTracking["Level 1 spell slots"] -= 1
        else:
            raise ValueError("Level 1 spell slots less than 1")
        return output

    def firebolt(self, targets):
        output = "Firebolt:\n"
        target = self.pickSingleTarget(targets, Monster)
        output+= self.rangedSpellAttack(target, 10, addvantage=targets[0].isAdvantage)
        return output

    def tollTheDead(self, targets):
        output = "Toll The-Dead:\n"
        target = self.pickSingleTarget(targets, Monster)
        if target.rollD20(addvantage=target.isAdvantage)+target.wizdom > 8+self.profMod+self.inteligence:
            output += "\thits" + target.name +"\n"
            if target.HP < target.maxHP//2:
                target.takeDamage(self.rollDX(12))
            else:
                target.takeDamage(self.rollDX(8))
        else:
            output += "\tmisses" + target.name +"\n"
        return output

    def rangedSpellAttack(self, target, damage, addvantage=False, disadvantage=False):
        if target.AC <= self.rollD20(addvantage=addvantage, disadvantage=disadvantage)+self.inteligence+self.profMod:
            target.takeDamage(self.rollDX(damage)+self.inteligence)
            return "hits"
        return "misses"

    def fighter(self, level):
        self.AC = 16  # Chainmail
        self.meleeDam = 8  # Longsword
        self.AC += 2  # sheild
        self.rangedRange = 150  # Javelins
        self.rangedDam = 8
        self.meleeDam += 2 # Dueling fighting style
        self.abilityTracking.update({"second wind": 1})
        self.bonusActions.update({"second wind": self.secondWind})

    def secondWind(self, targets):
        output = "Second Wind:\n"
        if self.abilityTracking.get("second wind") > 0:
            self.HP += self.rollDX(10)+self.level
            if self.HP > self.maxHP:
                self.HP = self.maxHP
            self.abilityTracking["second wind"] -= 1

        else:
            raise ValueError("Second wind less than 0")
        return output



    def meleeAttack(self, targets, addvantage=False, disadvantage=False):
        output = "melee attack: \n"
        target = self.pickAjecentTarget(targets, Monster)
        if target.AC <= self.rollD20(addvantage=target.isAdvantage)+self.strength+self.profMod:
            output += "\thits" + target.name +"\n"
            target.takeDamage(self.rollDX(self.meleeDam)+self.strength)
        else:
            output += "\tmisses" + target.name +"\n"
        return output
    def rangedAttack(self, targets):
        output = "ranged attack: \n"
        try:
            self.pickAjecentTarget(targets, Monster)
            disadvantage = True

        except ValueError:
            disadvantage = False

        target = self.pickSingleTarget(targets, Monster)
        if target.AC <= self.rollD20(addvantage=target.isAdvantage, disadvantage=disadvantage)+self.strength+self.profMod:
            target.takeDamage(self.rollDX(self.meleeDam)+self.strength)
            output += "\thits" + target.name +"\n"
        else:
            output += "\tmisses" + target.name +"\n"
        return output