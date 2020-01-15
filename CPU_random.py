from itertools import chain
import API
import random

def random_square(grid):
    # Find which squares are empty
    empty = API.get_empty(grid)
    choice = random.choice(empty)
    #print(empty, choice)
    return choice


if __name__ == '__main__':
    API.create_game('CPU', random_square)