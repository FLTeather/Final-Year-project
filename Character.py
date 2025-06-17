from Creature import Creature
class Character(Creature):
    def __init__(self, name, HP, AC, passPerc, battelfield, stre, dex, con, inte, wiz, char, klass, level):
        Creature.__init__(self, name, HP, AC, passPerc, battelfield, stre, dex)
        self.wizdom = wiz
        self.charisma = char
        self.inteligence = inte
        self.consitution = con
        self.assignClass(klass, level)
        self.meleeRange = 1
        self.meleeDam = 4
        self.rangedRange = 10
        self.rangedDam = 4
        self.abilityTracking = {} #ability name : usesleft
        self.level = level
        self.actions.update({"ranged attack": self.rangedAttack})

    def assignClass(self, klass, level):
        self.classes = {"cleric": self.paladin, "wizard": self.wizard, "fighter": self.fighter}
        if klass in self.classes.keys():
            self.classes[klass.lower()](level)
        else:
            raise ValueError("Unknown class '{}'".format(klass))

    def paladin(self, level):
        print("paladin")
        self.AC = 16 # Chainmail
        self.meleeDam = 8 #Longsword
        self.AC += 2 #sheild
        self.rangedRange = 30 # Javelins
        self.rangedDam = 6
        self.abilityTracking.update({"divine sense": 1+self.charisma})
        self.actions.update({"divine sense": self.divineSense})
        self.abilityTracking.update({"layOnHands": level*5})
        self.actions.update({"layOnHands": self.layOnHands})


    def divineSense(self):
        if self.abilityTracking.get("divine sense") > 0:
            self.abilityTracking["divine sense"] -= 1
            return [creature for creature in self.battelfield.allSeenCreatures(self, ranged=60) if creature.type in ["celestial", "fiend", "undead"]]
        else:
            raise ValueError("Divine sense less than 0")

    def layOnHands(self, amount, targetY, targetX):
        if self.abilityTracking.get("layOnHands") >= amount:
            self.battelfield.dealDamage(targetY, targetX, amount*-1)
            self.abilityTracking["layOnHands"] -= amount
        else:
            raise ValueError("Lay-on hands less than {}".format(amount))


    def wizard (self, level):
        print("wizard")
        self.meleeDam = 6 #Quaterstaff

        self.actions.pop("ranged attack")
        # No need to add arcne recovery as it only applies outside of combat.
        self.abilityTracking.update({"Level 1 spell slots":2})
        self.actions.update({"firebolt": self.firebolt})
        self.actions.update({"tollTheDead": self.tollTheDead})
        # 6 level one spells are known but only two spell slots, let us assume that 2 of these spells that have no use in combat
        # Feather fall, detect magic and
        self.actions.update({"magicMissile": self.magicMissile})
        self.actions.update({"mage armour": self.mageArmour})
        self.actions.update({"burning hands": self.burningHands})
    def mageArmour(self):
        if self.abilityTracking.get("Level 1 spell slots") >0:
            self.abilityTracking["Level 1 spell slots"] -= 1
            self.AC = 16
        else:
            raise ValueError("Level 1 spell slots less than 1")

    def magicMissile(self, target1, target2, target3):
        if self.abilityTracking.get("Level 1 spell slots") >0:
            target1.takeDamage(self.rollDX(4)+1)
            target2.takeDamage(self.rollDX(4)+1)
            target3.takeDamage(self.rollDX(4)+1)
            self.abilityTracking["Level 1 spell slots"] -= 1
        else:
            raise ValueError("Level 1 spell slots less than 1")

    def burningHands(self, targets):
        if self.abilityTracking.get("Level 1 spell slots") >0:
            pass
            damage = self.rollDX(6)+self.rollDX(6)+self.rollDX(6)
            for target in targets:
                y, x = target.getYX()
                self.battelfield.dealDexSaveDamage(y, x, damage)
        else:
            raise ValueError("Level 1 spell slots less than 1")
    def firebolt(self, target, addvantage=False, disadvantage=False):
        self.rangedSpellAttack(target, 10, addvantage, disadvantage)

    def tollTheDead(self, target, addvantage=False, disadvantage=False):
        if target.rollD20(addvantage=target.hasAdvantage)+target.wizdom > 8+self.profMod+self.inteligence:
            if target.HP < target.maxHP//2:
                target.takDamage(self.rollDX(12))
            else:
                target.takDamage(self.rollDX(8))

    def rangedSpellAttack(self, target, damage, addvantage=False, disadvantage=False):
        if target.ac <= self.rollD20(addvantage=addvantage, disadvantage=disadvantage)+self.inteligence+self.profMod:
            target.takeDamage(self.rollDX(damage)+self.inteligence)

    def fighter(self, level):
        self.AC = 16  # Chainmail
        self.meleeDam = 8  # Longsword
        self.AC += 2  # sheild
        self.rangedRange = 150  # Javelins
        self.rangedDam = 8
        self.meleeDam += 2 # Dueling fighting style
        self.abilityTracking.update({"second wind": 1})
        self.bonusActions.update({"second wind": self.secondWind})

    def secondWind(self):
        if self.abilityTracking.get("second wind") > 0:
            self.HP += self.rollDX(10)+self.level
        else:
            raise ValueError("Second wind less than 0")

    def meleeAttack(self, target, addvantage=False, disadvantage=False):
        if target.ac <= self.rollD20(addvantage=addvantage, disadvantage=disadvantage)+self.strength+self.profMod:
            target.takeDamage(self.rollDX(self.meleeDam)+self.strength)

    def rangedAttack(self, target, addvantage=False, disadvantage=False):
        if target.ac <= self.rollD20(addvantage=addvantage, disadvantage=disadvantage)+self.strength+self.profMod:
            target.takeDamage(self.rollDX(self.meleeDam)+self.strength)

Character("rob", 5, 5, 10, "IDC", 1, 2, 3, 4, 5, 6, "widard", 1)