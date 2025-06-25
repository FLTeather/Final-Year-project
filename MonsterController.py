class MonsterController:
    def __init__(self, board, creature, parent=None, parent_action=None):
        self.state = board
        self.creature = creature
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self.number_of_visits = 0
        self.damage = {"delt":0, "taken":0}
        self.untried_actions = [30, "action", "bonus"]
        self.untried_actions = self.untried_actions2()
        return

    def untried_actions2(self):
        if self.parent_action is None:
            return self.untried_actions
        return self.untried_actions

    def resultDiffernece(self):
        return self.damage["delt"] - self.damage["taken"]

    def getNumberOfVisits(self):
        return self.number_of_visits

    def exspand(self):
        pass

    def pickAction(self):
        pass
