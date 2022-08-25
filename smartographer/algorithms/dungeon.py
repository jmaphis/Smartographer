# A dungeon generation algorithm by James Maphis
# The dungeon object creates a 2 dimensional array of 1s and 0s, which
# represent floor and wall tiles in a dungeon, respectively.
from smartographer.utilities.seedmanager import SeedManager


class Dungeon():

    # Generates a dungeon in the style of classic roguelike games
    def __init__(self, width: str, height: int,
                room_size_range: tuple[int, int], 
                room_count: int, seed: SeedManager):

        self.width = width
        self.height = height
        self.room_size_range = room_size_range
        self.room_count = room_count
        self.seed = seed

        self.room_list = []
        self.hall_list = []

        self.matrix = []
        for _ in range(self.width):
            column = []
            for _ in range(self. height):
                column.append(0)
            self.matrix.append(column)

    def generate_rooms(self):
        # generate a list of rooms, each with a random size and location
        while len(self.room_list) < self.room_count:

            # get a width and height for the room
            room_width = (self.seed.randint(self.room_size_range[0], 
                                        self.room_size_range[1]))
            room_height = (self.seed.randint(self.room_size_range[0], 
                                        self.room_size_range[1]))
            # get an x and y coords for the left and top sides, respectively
            left = self.seed.randint(0, self.width - room_width)
            top = self.seed.randint(0, self.height - room_height)
            # create a room object from the above values
            new_room = Room(left, (left + room_width), 
                        top, (top + room_height), self.seed)
                
            if len(self.room_list) != 0:
                for checks, room in enumerate(self.room_list):
                    if new_room.collide(room):
                        break
                    elif checks >= len(self.room_list) - 1:
                        self.room_list.append(new_room)
                        new_room.draw(self.matrix)

            else:
                self.room_list.append(new_room)
                new_room.draw(self.matrix)

    def get_hall_path(self, start_coords, end_coords):

        # allows the hallways to generate backwards if the end point is 
        # above or to the left of the start point by using a negative step
        if start_coords[0] <= end_coords[0]:
            step_x = 1
        else:
            step_x = -1
        if start_coords[1] <= end_coords[1]:
            step_y = 1
        else:
            step_y = -1

        start_direction = self.seed.choice(('horizontal', 'vertical'))
        if start_direction == 'horizontal':
            for tile in range(start_coords[0], end_coords[0], step_x):
                # moving left/right
                self.matrix[tile][start_coords[1]] = 1
            for tile in range(start_coords[1], end_coords[1], step_y):
                # moving up/down
                self.matrix[end_coords[0]][tile] = 1
        if start_direction == 'vertical':
            for tile in range(start_coords[1], end_coords[1], step_y):
                # moving up/down
                self.matrix[start_coords[0]][tile] = 1
            for tile in range(start_coords[0], end_coords[0], step_x):
                # moving left/right
                self.matrix[tile][end_coords[1]] = 1

    def generate_halls(self):

        self.room_list.sort(key=lambda room: 
            room.center()[0] +room.center()[1])
        for index, room in enumerate(self.room_list):
            if room != self.room_list[-1]:
                next_room = self.room_list[index - 1]
                self.get_hall_path(room.center(), next_room.random_coords())

    def generate(self):
        self.generate_rooms()
        self.generate_halls()

    def get_matrix(self):
        return self.matrix


class Room():

    def __init__(self, left: int, right: int, top: int, 
                       bottom: int, seed: SeedManager):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.width = self.right - self.left
        self.height = self.bottom - self.top
        self.seed = seed

    def center(self):
        # returns a list  containing the left and right
        # coords of the center of the room

        center_x = self.left + (self.width // 2)
        center_y = self.top + (self.height // 2)
        return [center_x, center_y]

    def collide(self, other_room):
        for x in range(self.left, self.right + 1):
            if other_room.left <= x <= (other_room.right + 1):
                for y in range(self.top, self.bottom + 1):
                    if other_room.top <= y <= (other_room.bottom + 1):
                        return True
        return False

    def draw(self, matrix):
        # takes a 2d array as an argument and sets the value of any 
        # tiles within the room to one.
        for x in range(self.width):
            for y in range(self.height):
                matrix[self.left + x][self.top + y] = 1

    def random_coords(self):
        # get a tuple of x and y coordinates for a random point within the room
        coord_tuple = (
        (self.seed.randint(self.left, self.right)),
        (self.seed.randint(self.top, self.bottom)))
        return coord_tuple

                
if __name__ == '__main__':
    # generates and prints a matrix for testing purposes.
    # these numbers are a recommended default.
    GRID_WIDTH = 60
    GRID_HEIGHT = 30
    ROOM_RANGE = (6, 10)
    ROOM_COUNT = 6

    map = Dungeon(GRID_WIDTH, GRID_HEIGHT, ROOM_RANGE, ROOM_COUNT)
    map.generate()
    print(map.matrix)
