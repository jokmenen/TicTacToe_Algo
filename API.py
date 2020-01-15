from itertools import chain
import random

CPUSYMBOL = ['@','&'] # Make this nonalphabetic so the player cannot pick it
EMPTYSYMBOL = '' # Symbol denoting the empty squares


# Shows the empty spaces in a grid using a list of coordinate tuples
def get_empty(grid):
    rowlen = len(grid[0])
    flatgrid = chain.from_iterable(grid)
    empty = []
    for i, sq in enumerate(flatgrid):
        # print([(i // rowlen, i % rowlen)])
        if sq == '':
            empty += [(i // rowlen, i % rowlen)]  # get coords of empty squares
    return empty


def create_game(gamemode = 'Local', cpu_func = None):
    gamemodes = ['Local', 'CPU', '2CPU']
    if gamemode not in gamemodes:
        print(f'Invalid gamemode entered: {gamemode}')
        return False
    grid = [[EMPTYSYMBOL, EMPTYSYMBOL, EMPTYSYMBOL, ] for _ in range(3)]
    players = {}

    if gamemode == 'Local':
        for p in range(2):
            p += 1
            name = f'Player {p}'
            players[create_player(name)] = name


    if gamemode == 'CPU':
        if cpu_func == None:
            'Invalid CPU Choice function!'
            return False
        cpu_func = [cpu_func]
        name = 'Player 1'
        players[create_player(name)] = name
        players[CPUSYMBOL[0]] = 'CPU'

    if gamemode == '2CPU':
        if type(cpu_func) != list:
            print('Invalid CPU Choice function! Select two CPU functions in 2CPU mode!')
            return False
        players[CPUSYMBOL[0]] = 'CPU'
        players[CPUSYMBOL[1]] = 'CPU2'


    firsttime = True
    while True:
        for symbol, player_name in players.items():

            if firsttime: # Decide randomly who starts if it's the first turn
                firsttime = False
                if random.choice([True,False]):
                    continue


            pp_grid(grid)
            print(f"{player_name}'s turn!")
            if symbol in CPUSYMBOL:
                cpu = ''.join(CPUSYMBOL).find(symbol)
                row, col = cpu_func[cpu](grid)
                grid = insert_symbol(symbol, grid, row, col)
            else:
                print('Put your symbol in an empty square: (row,col)')
                grid = insert_symbol(symbol, grid)

            if checkWin(grid):
                print(f'{player_name} won. Congratulations!')
                return
            if len(get_empty(grid)) == 0:
                print("The grid is full: Draw!")
                return

def insert_symbol(symbol, grid, row = None, col = None):
    newgrid = grid

    if not (row == None and col==None):
        newgrid[row][col] = symbol
        return newgrid
    else:
        while True:
            try:

                row = int(input('What row do you want to put your square in?'))
                col = int(input('What column do you want to put your square in?'))
            except ValueError:
                print("Not an integer! Try again.")
                continue
            if row > len(grid[0])-1 or col > len(grid)-1:
                print("Please insert a valid square")
                continue
            elif grid[row][col] == '':
                newgrid[row][col] = symbol
                return newgrid
            else:
                print(f"That square already contains a {newgrid[row][col]}")

        return newgrid

def create_player(name = None):
    if name:
        print(f"Creating {name}")
    player = ''
    while player == '':
        sym = input('Enter a letter symbol:').lower()[0]
        if not sym.isalpha():
            print('Not a letter. Try again please.')
        else:
            player = sym
    print(f'{name} plays as {player}!\n')
    return player


def pp_grid(grid):
    x = len(grid[0])
    length = len(grid)
    for y in range(length):
        print('|',*['{}|'.format(x) if x else ' |' for x in grid[y]], sep='')

# Define wincondition
def checkWinThree(symbol, row):
    occurrences = [i for i, x in enumerate(row) if x == symbol]
    if len(occurrences) == len(row):
        return True
    else:
        return False


# A player wins if they have three symbols in a row, column or diagonal.
def checkWin(grid):
    symbols = set(chain.from_iterable(grid))
    if EMPTYSYMBOL in symbols:
        symbols.remove(EMPTYSYMBOL)
    # Check all rowsm
    for row in grid:
        for symbol in symbols:
            if checkWinThree(symbol, row):
                return symbol

    # Check all columns (Note: assumes all rows and columns are equally long)
    for colnr in range(len(grid[0])):
        for symbol in symbols:
            col = [grid[row][colnr] for row in
                   range(len(grid))]  # get the colnr'th element from each row to get current column
            if checkWinThree(symbol, col):
                return symbol

    # Check the diagonals
    diag_asc  = [grid[0][2], grid[1][1], grid[2][0]]
    diag_desc = [grid[0][0], grid[1][1], grid[2][2]]

    for diag in (diag_asc,diag_desc):
        for symbol in symbols:
            if checkWinThree(symbol, diag):
                return symbol

    return False



if __name__ == '__main__':
    #create_game()
    grid = [['', '', ''], ['', '', ''], ['', '', '']]
    print(get_empty(grid))