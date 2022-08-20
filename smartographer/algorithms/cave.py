# A cave generation agorythm by James Maphis.
# The cave object creates a 2 dimensional array of 1s and 0s, which
# represent floor and wall tiles in a cave, respectively.
# Uses a "Random Walk" style algorithm.
import random


class Cave:

    # generates a cave map using the 'Random Walk' technique
    def __init__(self, grid_width: int, grid_height: int, cave_size: int, centered=False):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cave_size = cave_size

        self.matrix = []
        for x in range(self.grid_width):
            column = []
            for y in range(self.grid_height):
                column.append(0)
            self.matrix.append(column)      

    def valid_step(self, walker, step):
        # checks if the next step is within list range
        if step == 'left':
            if walker['x'] - 1 < 0:
                return False
        if step == 'right':
            if walker['x'] + 1 >= self.grid_width:
                return False
        if step == 'up':
            if walker['y'] - 1 < 0:
                return False
        if step == 'down':
            if walker['y'] + 1 >= self.grid_height:
                return False
        return True

    def generate_centered(self):
        # an alternate algorithm for a tighter, more centered cave
        # place out walker in roughly the middle of the matrix
        walker = {'x': self.grid_width // 2, 'y': self.grid_height // 2}
        steps = 0
        # change the value at the starting tile
        self.matrix[walker['x']][walker['y']] = 1

        while steps < self.cave_size:
            # pick a random direction and adjust the walker's position
            axis = random.choice(('x', 'y'))

            if axis == 'x':
                roll = random.randrange(self.grid_width)
                if roll < walker['x']:
                    walker['x'] -= 1
                else:
                    walker['x'] += 1
            if axis == 'y':
                roll = random.randrange(self.grid_height)
                if roll < walker['y']:
                    walker['y'] -= 1
                else:
                    walker['y'] += 1

            if self.matrix[walker['x']][walker['y']] == 0:
                steps += 1
                # change the value at the walker's new position
            self.matrix[walker['x']][walker['y']] = 1

    def generate(self):
        # place our random walker in roughly the middle of the array
        walker = {'x': self.grid_width // 2, 'y': self.grid_height // 2}
        directions = ['left', 'right', 'up', 'down']
        steps = 0
        # change the value at the walker's position
        self.matrix[walker['x']][walker['y']] = 1

        while steps < self.cave_size:
            # pick a random direction and adjust the walker's position
            direction = random.choice(directions)
            if self.valid_step(walker, direction):

                if direction == 'left':
                    walker['x'] -= 1
                if direction == 'right':
                    walker['x'] += 1
                if direction == 'up':
                    walker['y'] -= 1
                if direction == 'down':
                    walker['y'] += 1

                if self.matrix[walker['x']][walker['y']] == 0:
                    steps += 1
                # change the value at the walker's position
                self.matrix[walker['x']][walker['y']] = 1
            else:
                walker = {'x': self.grid_width // 2,
                          'y': self.grid_height // 2}

    def get_matrix(self):
        return self.matrix
        print("testing")


if __name__ == '__main__':
    # generates and prints a matrix for testing purposes.
    # these numbers are a recommended default.
    GRID_WIDTH = 60
    GRID_HEIGHT = 30
    CAVE_SIZE = 750

    map = Cave(GRID_WIDTH, GRID_HEIGHT, 750)
    map.generate()
    print(map.get_matrix())
