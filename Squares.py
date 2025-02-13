class Squares:
    def __init__(self, creature=None, wallNorthSouth=False, wallEastWest=False, difficultTerain=False, height=0):
        self.creature = creature
        self.wallNorthSouth = wallNorthSouth
        self.wallEastWest = wallEastWest
        self.difficultTerain = difficultTerain
        self.height = height

    def __repr__(self):
        if self.creature is not None:
            return f' {self.creature.name} '
        if self.wallNorthSouth:
            return "|"
        if self.wallEastWest:
            return "─"
        return "."