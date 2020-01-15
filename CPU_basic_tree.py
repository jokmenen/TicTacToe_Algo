from itertools import chain
import API
from API import CPUSYMBOL
import CPU_random
from copy import deepcopy
import operator

DEPTH = 1000

# TODO Do monte carlo tree search instead
#  1 Check possibilities
#  Recursive search for depth specified to find best move

# Simulate a game while choosing the moves for both players using the policy specified
# Note that the simulation will begin with the second symbol specified (since the tree function already
# made a move for that player), and return a 1 if that player wins.
def simulate(grid, policy, symbols = CPUSYMBOL[0]):

    # Who should return a positive or negative reward if they win
    CPU_pos = symbols[1]
    CPU_neg = symbols[0]


    available = API.get_empty(grid)
    # Qhile there are empty squares, pick one using the policy. Keep going until all squares are filled or a player won
    while available:
        # get best square using policy
        choice = policy(grid)
        # place symbol in square
        grid = API.insert_symbol(symbols[0], grid, *choice)
        #API.pp_grid(grid)
        # evaluate board
        win = API.checkWin(grid)
        if win == CPU_pos:
            return 1
        elif win == CPU_neg:
            return -1

        # switch symbols
        symbols.reverse()
        #print(symbols)
        # repeat
        available = API.get_empty(grid)
        #print(available)
    return 0

def get_opponent(grid, cpu = CPUSYMBOL[0]): # Get the symbol for the opponent. Returns 'x' if none found.
    symbols = set(chain.from_iterable(grid))
    if API.EMPTYSYMBOL in symbols:
        symbols.remove(API.EMPTYSYMBOL)
    if cpu in symbols: #TODO fix 2CPU?
        symbols.remove(cpu)
    if len(symbols) == 1:
        return list(symbols)[0]
    else:
        return 'x'

def tree(grid, cpu = CPUSYMBOL[0]):

    # Check available moves
    available = API.get_empty(grid)

    score_dict = {}
    opponent_symbol = get_opponent(grid, cpu)

    # For each of the possible moves at this point, simulate some games to evaluate the score of each move
    for choice in available:
        choice_grid = deepcopy(grid)
        choice_grid = API.insert_symbol(cpu,choice_grid,*choice)

        win = API.checkWin(choice_grid)

        if win == cpu:  # Direct win --> best choice
            return choice

        choice_score = 0
        for sim in range(DEPTH): # Run simulations until the depth limit is reached
            sim_grid = deepcopy(choice_grid)
            choice_score += simulate(sim_grid,CPU_random.random_square,[opponent_symbol,'@'])
        score_dict[choice] = choice_score

    print('Move evaluation:', score_dict)

    return max(score_dict.items(), key=lambda x: x[1])[0]

if __name__ == '__main__':
    API.create_game('2CPU', [tree,tree])
    # grid = [['', '', ''], ['', '', ''], ['', '', '']]
    # API.pp_grid(grid)
    # print(tree(grid))