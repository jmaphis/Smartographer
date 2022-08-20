# A world generation algorithm by James Maphis
# The World object creates a 2 dimensional array of 1s and 0s, which
# represent water and land tiles on a world map, respectively.
# Uses cellular automata to turn a random distribution of "land" and
# "water" into oceans and land masses.
import random
from copy import deepcopy


class World():

    # Generates a world map using cellular automata
    def __init__(self, grid_width: int, grid_height: int,
                 density: int, smoothing=2):

        self.grid_width = grid_width
        self.grid_height = grid_height
        self.density = density
        self.smoothing = smoothing

    def generate(self):

        # creates a matrix filled randomly with 1s and 0s
        self.matrix = []
        for x in range(self.grid_width):
            column = []
            for y in range(self.grid_height):
                if x not in (0, self.grid_width) and\
                        y not in (0, self.grid_height):
                    roll = random.randint(0, 100)
                    if roll < self.density:
                        column.append(1)
                    else:
                        column.append(0)
                else:
                    column.append(0)
            self.matrix.append(column)

        self.next_generation = deepcopy(self.matrix)

        # applies cellular automata to group land tiles into islands
        for _ in range(self.smoothing):
            self.smooth_world()

    def is_border(self, x_coord, y_coord):

        # checks if a tile is on the edge of the map
        return x_coord == 0 or x_coord == self.grid_width - 1 \
            or y_coord == 0 or y_coord == self.grid_height - 1

    def smooth_world(self):

        # counts the tiles around the each tile to determine if it will
        # be land or water in the next generation.
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                population = 0
                if self.is_border(x, y):
                    pass
                else:
                    left_coord = (x - 1)
                    right_coord = (x + 1)
                    above_coord = (y - 1)
                    below_coord = (y + 1)

                    population = 0
                    if self.matrix[left_coord][above_coord] == 1:
                        population += 1
                    if self.matrix[x][above_coord] == 1:
                        population += 1
                    if self.matrix[right_coord][above_coord] == 1:
                        population += 1
                    if self.matrix[left_coord][y] == 1:
                        population += 1
                    if self.matrix[right_coord][y] == 1:
                        population += 1
                    if self.matrix[left_coord][below_coord] == 1:
                        population += 1
                    if self.matrix[x][below_coord] == 1:
                        population += 1
                    if self.matrix[right_coord][below_coord] == 1:
                        population += 1

                if population >= 4:
                    # these tiles will be land
                    self.next_generation[x][y] = 1
                else:
                    # these tiles will be water
                    self.next_generation[x][y] = 0
            # replaces the current generation with the next
            self.matrix = deepcopy(self.next_generation)

    def get_matrix(self):
        return self.matrix


if __name__ == '__main__':
    # generates and prints a matrix for testing purposes.
    # these numbers are a recommended default.
    # increasing the default kwarg "smoothing" beyond one
    # will result in a more rounded world. setting it higher
    # than 4 is not recommended
    GRID_WIDTH = 120
    GRID_HEIGHT = 60
    DENSITY = 38

    map = World(GRID_WIDTH, GRID_HEIGHT, DENSITY)
    map.generate()
    print(map.matrix)
