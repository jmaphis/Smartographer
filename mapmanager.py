from algorithms.cave import Cave
from algorithms.dungeon import Dungeon
from algorithms.world import World
from copy import deepcopy

class MapManager():

    def __init__(self, width, height, args=None, style='normal'):
        self.style = style
        self.width = width
        self.height = height
        self.args = args


    def get_map(self, type):
        if type == 'cave':
            new_map = Cave(self.width, self.height, 750)
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
        '''template_map = []
        for x, column in enumerate(map):
            template_column = []
            for y, tile in enumerate(column):
                template_column.append(self.get_divs(map, tile, type))
            template_map.append(template_column)
        return template_map'''

    def get_divs(self, tile, type):
        if type == 'cave':
            if tile == 1:
                if self.style == 'normal':
                    return '<div class="grey"></div>'
            else:
                if self.style == 'normal':
                    return '<div class="black"></div>'
        if type == 'dungeon':
            if tile == 1:
                if self.style == 'normal':
                    return '<div class="grey"></div>'
            else:
                if self.style == 'normal':
                    return '<div class="black"></div>'
        if type == 'world':
            if tile == 1:
                if self.style == 'normal':
                    return '<div class="green"></div>'
            else:
                if self.style == 'normal':
                    return '<div class="blue"></div>'

if __name__ == "__main__":
    manager = MapManager(30, 60)
    test_map = manager.get_map('cave')
    print("finished product: ")
    print(test_map)
    print(manager.get_map('cave'))
