from smartographer.algorithms.cave import Cave
from smartographer.algorithms.dungeon import Dungeon
from smartographer.algorithms.world import World

from copy import deepcopy

class MapManager():
    # handles the creation of maps, and fills their matrices with html

    def __init__(self, width, height, args=None, style='normal'):
        self.style = style
        self.width = width
        self.height = height
        self.args = args

    def get_map(self, type):
        if type == 'cave':
            new_map = Cave(self.width, self.height, 750)
            new_map.generate()
            new_map = self.convert(new_map.get_matrix(), type)
        if type == 'dungeon':
            new_map = Dungeon(self.width, self.height, (9, 15), 6)
            new_map.generate()
            new_map = self.convert(new_map.get_matrix(), type)
        if type == 'world':
            new_map = World(self.width, self.height, 40)
            new_map.generate()
            new_map = self.convert(new_map.get_matrix(), type)

        return new_map

    def convert(self, map, type):
        template_map = deepcopy(map)
        for x, column in enumerate(map):
            for y, tile in enumerate(column):
                template_map[x][y] = self.get_divs(tile, type)
        return template_map

    def get_divs(self, tile, type):
        if type == 'cave' or type == 'dungeon':
            if tile == 1:
                if self.style == 'normal':
                    return '<div class="grey tile"></div>'
            else:
                if self.style == 'normal':
                    return '<div class="black tile"></div>'
        if type == 'world':
            if tile == 1:
                if self.style == 'normal':
                    return '<div class="green tile"></div>'
            else:
                if self.style == 'normal':
                    return '<div class="blue tile"></div>'

if __name__ == "__main__":
    manager = MapManager(30, 60)
    test_map = manager.get_map('cave')
    print("finished product: ")
    print(test_map)
    print(manager.get_map('cave'))
