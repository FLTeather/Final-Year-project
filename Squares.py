class Squares:
    def __init__(self, creature=None, wallNorthSouth=False, isWall=False, height=0):
        self.creature = creature
        self.wallNorthSouth = wallNorthSouth
        self.isWall = isWall
        self.height = height

    def __repr__(self):
        if self.creature is not None:
            return f'{self.creature.name}'
        if self.isWall:
            return "W"
        return "."