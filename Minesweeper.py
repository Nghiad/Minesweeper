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
        command = input("Change mode or pick next position. ").strip()
        if command == 'dig' or command == 'DIG' or command == 'Dig':
            return 'dig'
        elif command == 'flag' or command =='FLAG' or command == 'Flag':
            return 'flag'
        else:
            command = command.split()
            if command[0].isdigit():
                x = int(command[0])
                y = int(ascii_letters.index(command[1]))
            else:
                y = int(ascii_letters.index(command[0]))
                x = int(command[1])
            return (x-1, y)

    except:
        return None                                                 #returns coordinates

def dig(pboard, mboard, pos):
    if mboard[pos[0]][pos[1]] == '-' and pboard[pos[0]][pos[1]] != '-':
        pboard[pos[0]][pos[1]] = mboard[pos[0]][pos[1]]
        for row in range(max(0, (pos[0]-1)), min((pos[0]+2), len(pboard))):
            for column in range(max(0, (pos[1]-1)), min((pos[1]+2), len(pboard))):
                if pboard[row][column] == '-' or (row,column) == pos:
                    continue
                elif mboard[row][column] == '-' and pboard[row][column] != '-':
                    dig(pboard, mboard, (row, column))
                pboard[row][column] = mboard[row][column]
    pboard[pos[0]][pos[1]] = mboard[pos[0]][pos[1]]

def flag(pboard, pos):
    if pboard[pos[0]][pos[1]] == 'F':
        pboard[pos[0]][pos[1]]= 0
    elif pboard[pos[0]][pos[1]] == 0:
        pboard[pos[0]][pos[1]]= 'F'


#Default settings
x = 15
y = 40
mode = 'DIG'

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

    print_board(masterboard)                #FOR TESTING!!!!

    while True:
        print ()
        print_board(playerboard)
        print ()
        print ("MODE: ", mode)
        print ()
        location = get_pos()
        if location == 'dig':
            mode = 'DIG'
        elif location == 'flag':
            mode = 'FLAG'
        else:
            if mode == 'DIG':
                dig(playerboard, masterboard, location)
            elif mode == 'FLAG':
                flag(playerboard, location)

