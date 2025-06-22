# This class will handle the turn choice which is why it looks so empty right now.
from Character import Character
class PlayerController:
    def __init__(self, board):
        self.characters = []
        self.board = board

    def addMonster(self, character):
        self.character.append(character)
        character.monsterController = self
    def takeTurn(self):
        creature = self.board.nextTurn()

    def calulateTurn(self):
        CharacterPostions = [[creature, (creature.getYX())] for creature in self.board.allCreatures if type(creature) == Character]
        MonsterPostions = [[creature, (creature.getYX())] for creature in self.board.allCreatures if type(creature) == Monster]
        print(CharacterPostions)
        print(MonsterPostions)
        print(self.wizardScore(CharacterPostions[0][0], MonsterPostions))

    def wizardScore(self, wizard, monsters):
        count = 0
        adjecentSquares = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        wizardSqaure = wizard.getYX()
        allSqaures = [(wizardSqaure[0]+x[0], wizardSqaure[1]+x[1]) for x in adjecentSquares]
        for monster in monsters:
            for move in monster[0].allMoves:
                if move in allSqaures:
                    count += 1
                    break
        return count

    def exspectedDamage(self, AC, attackMod):
        return (21- (AC-attackMod)/20)*100


    def pickBestMove(self, dataStructure):
        pass