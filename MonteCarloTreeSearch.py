from Battelfield import Battelfield
from Creature import Creature
from copy import deepcopy
from random import choice
import numpy as np

class MonteCarloTreeSearch:
    def __init__(self, board:Battelfield, parent=None, lastMove=None, isMonster=False):
        self.parent = parent
        self.children = []
        self.isMonster = isMonster
        self.board = board
        self.creatureTurn:Creature = board.currentTurn()[1]
        self.possibleActions = deepcopy(self.creatureTurn.actions)
        self.possibleBonus = deepcopy(self.creatureTurn.bonusActions)
        self.possibleMoves = []
        self.speedLeft = self.creatureTurn.turnSpeed
        self.winLoss = [1, 1]
        if self.speedLeft > 0:
            self.possibleMoves = self.creatureTurn.getAllAdjecentMoves()
        self.fullExspanded = False

        self.terminal = False
        if self.board.winCondision() != 2:
            self.terminal = True
            self.backPropagate(self.board.winCondision())
        if lastMove is None:
            lastMove = [None]
        self.lastMove = lastMove


    def expandv2(self):
        #print("expsand v2")
        newBoard = deepcopy(self.board)
        if len(self.possibleMoves) == 0 and len(self.possibleBonus) == 0 and len(self.possibleActions) == 0:
            self.fullExspanded = True
            newBoard.nextTurn()
            self.children.append(MonteCarloTreeSearch(newBoard, self, isMonster=self.isMonster))
            return
        newCreature:Creature = newBoard.currentTurn()[1]

        if len(newCreature.choices) == 0:
            self.fullExspanded = True
            newBoard.nextTurn()
            self.children.append(MonteCarloTreeSearch(newBoard, self, isMonster=self.isMonster))
            return

        if len(self.possibleActions) == 0 and "action" in newCreature.choices:
            newCreature.choices.remove("action")
        if len(self.possibleBonus) == 0 and "bonus" in newCreature.choices:
            newCreature.choices.remove("bonus")
        if len(self.possibleMoves) == 0 and "move" in newCreature.choices:
            newCreature.choices.remove("move")

        try:
            turnChoice = newCreature.choices[0]
        except IndexError:
            self.fullExspanded = True
            newBoard.nextTurn()
            self.children.append(MonteCarloTreeSearch(newBoard, self, isMonster=self.isMonster))
            return

        nextMove = None
        if turnChoice == "action":
            key = choice([key for key in self.possibleActions])
            self.possibleActions.pop(key)
            try:
                newCreature.actions[key](newBoard.allCreatures)
                newCreature.choices.remove(turnChoice)

            except ValueError:
                return

            nextMove = ["action", key]

        elif turnChoice == "bonus":
            key = choice([key for key in self.possibleBonus])
            self.possibleBonus.pop(key)
            try:
                newCreature.bonusActions[key](newBoard.allCreatures)
                newCreature.choices.remove(turnChoice)
            except ValueError:
                return
            nextMove = ["bonus", key]

        elif turnChoice == "move":
            move = choice(self.possibleMoves)
            self.possibleMoves.remove(move)
            newCreature.move(move[0], move[1])
            if newCreature.turnSpeed == 0:
                newCreature.choices.remove(turnChoice)
            nextMove = ["move", move]

        # At this point with have a creature that has done something

        # create child who took this move
        childBoard = deepcopy(newBoard)
        temp = MonteCarloTreeSearch(childBoard, self, nextMove, isMonster=self.isMonster)
        self.children.append(temp)
        temp.payout(newBoard)


        # simulate this move


    def payout(self, board):
        #print("Simulating")
        creature = board.currentTurn()
        creature[1].takeTurn()
        counter = 0
        while board.winCondision() == 2:
            counter += 1
            board.nextTurn()[1].takeTurn()
            # print(counter)
        self.backPropagate(board.winCondision())
        return

    def backPropagate(self, winOrLoss:int):
        #print("backpropagate" + str(self.winLoss))
        if self.isMonster:
            if winOrLoss == 1:
                self.winLoss[0] += 1
            elif winOrLoss == 0:
                self.winLoss[1] += 1
        else:
            self.winLoss[winOrLoss] += 1
        if self.parent == None:
            return
        self.parent.backPropagate(winOrLoss)
        return

    def selection(self):
        #print("Selection")
        if self.terminal:
            return self
        if not self.fullExspanded:
            self.expandv2()
            return
        return self.best_child().selection()

    def q(self):
        return self.winLoss[0] - self.winLoss[1]

    def n(self):
        return sum(self.winLoss)

    def best_child(self, c_param=0.3):
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]










