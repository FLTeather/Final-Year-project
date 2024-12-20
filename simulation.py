class simulation():
    def __init__(self, name, size_y, size_x):
        self.name = name
        self.world = [range(size_x) for x in range(size_y)]
        print(self.world)


simulation("test", 2, 2)

