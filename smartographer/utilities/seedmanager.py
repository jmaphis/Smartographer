# seedmanager - a modified version of the random module, 
# but based on one starting seed

import random


class SeedManager():
    def __init__(self, seed=None):
        print('seedmanager')
        print(seed)
        if seed:
            self.start_seed = seed
        else:
            self.start_seed = random.randrange(9999999)
        self.current_seed = self.start_seed

    def set_start_seed(self, seed: int):
        self.start_seed = seed
        self.current_seed = seed

    def get_start_seed(self):
        return self.start_seed

    def update_current(self):
        random.seed(self.current_seed)
        self.current_seed = random.randrange(99999999999999999)

    def choice(self, choice_list: list):
        random.seed(self.current_seed)
        roll = random.choice(choice_list)
        self.update_current()
        return roll

    def randrange(self, upper):
        random.seed(self.current_seed)
        roll = random.randrange(upper)
        self.update_current()
        return roll

    def randint(self, lower, upper):
        random.seed(self.current_seed)
        roll = random.randint(lower, upper)
        self.update_current()
        return roll

if __name__ == '__main__':
    pass