from random import randint
from string import ascii_letters


def new_board(size, x):
    board = [[x for column in range(size)] for row in range(size)]
    return board

def plant_bombs(board, numbombs):
    bombs = 0
    while bombs < numbombs:
        x = randint(0, len(board)-1)
        y = randint(0, len(board)-1)
        board[x][y] = '*'
        bombs += 1
    return board

def assign(board):
    for row in range(len(board)):
        for column in range(len(board)):
            if board[row][column] == '*' or check(board,(row,column)) == 0:
                continue
            board[row][column] = check(board,(row,column))
    return board

def print_board(board):
    print ("     ", end='')
    for alpha in range(len(board)):
        if alpha == (len(board)-1):
            print(ascii_letters[alpha])
        else:
            print(ascii_letters[alpha], end=" ")
    print ("    ", end=' ')
    for alpha in range(len(board)):
        if alpha == (len(board)-1):
            print('--')
        else:
            print('--', end="")

    for row in range(len(board)):
        for column in range(len(board[0])):
            if column == 0:
                print ('{:>3}'.format(row+1), "|", end='')
            if column == (len(board)-1):
                print(board[row][column], "|", row+1)
            else:
                print(board[row][column], end=' ')

    print ("     ", end='')
    for alpha in range(len(board)):
        if alpha == (len(board)-1):
            print('--')
        else:
            print('--', end="")
    print ("    ", end=' ')
    for alpha in range(len(board)):
        if alpha == (len(board)-1):
            print(ascii_letters[alpha])
        else:
            print(ascii_letters[alpha], end=" ")

def check(board, pos):
    n = 0
    for row in range(max(0, (pos[0]-1)), min((pos[0]+2), len(board))):
        for column in range(max(0, (pos[1]-1)), min((pos[1]+2), len(board))):
            if board[row][column] == '*':
                n += 1
    return n                         #return number of surrounding bombs

def get_pos():
    try:
        location = input("which position? ").strip().split()
        if location[0].isdigit():
            x = int(location[0])
            y = int(ascii_letters.index(location[1]))
        else:
            y = int(ascii_letters.index(location[0]))
            x = int(location[1])
        return (x, y)

    except:
        return None                                                 #returns coordinates

def dig(mboard, pboard, pos):
    pboard[pos[0]-1][pos[1]] = mboard[pos[0]-1][pos[1]]
    if pboard[pos[0]-1][pos[1]] == '-':
        for row in range(max(0, (pos[0]-1)), min((pos[0]+2), len(pboard))):
            for column in range(max(0, (pos[1]-1)), min((pos[1]+2), len(pboard))):
                if mboard[row][column] == '-' and not pboard[row][column] != '-':
                    dig(mboard, pboard, (row, column))
                pboard[row][column] = mboard[row][column]
                print_board(pboard)

#Default settings
x = 15
y = 40

if __name__=='__main__':
    print ("Separate by a space; Default is 15 40")
    print ("Maximum size is 50")
    while True:
        try:
            difficulty = input("Input board size and number of bombs: ").split()
            x = int(difficulty[0])
            y = int(difficulty[1])
            break
        except:
            print ("invalid")

    masterboard = assign(plant_bombs(new_board(x, '-'), y))
    playerboard = new_board(x, 0)

    print_board(masterboard)

    while True:
        print ()
        print_board(playerboard)
        print ()
        position = get_pos()
        if masterboard[position[0]][position[1]] == '*':
            print_board(masterboard)
            print ()
            print("you lost")
            break
        else:
            dig(masterboard, playerboard, position)

