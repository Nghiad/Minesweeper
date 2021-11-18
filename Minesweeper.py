from random import randint
from string import ascii_letters


def new_board(size, base):                                              #create blank board
    board = [[base for column in range(size)] for row in range(size)]
    return board

def plant_bombs(board, numbombs):                              #plant all bombs on board
    bombs = 0
    while bombs < numbombs:
        x = randint(0, len(board)-1)
        y = randint(0, len(board)-1)
        board[x][y] = '*'
        bombs += 1
    return board

def check(board, pos):                               #return number of surrounding bombs
    n = 0
    for row in range(max(0, (pos[0]-1)), min((pos[0]+2), len(board))):
        for column in range(max(0, (pos[1]-1)), min((pos[1]+2), len(board))):
            if board[row][column] == '*':
                n += 1
    return n 

def assign(board):                          #call check function and assignment on board
    for row in range(len(board)):                   
        for column in range(len(board)):
            if board[row][column] == '*' or check(board,(row,column)) == 0:
                continue
            board[row][column] = check(board,(row,column))
    return board

def print_board(board):                                    #print board in proper format
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

def get_pos(playerboard):                                   #checks if input mode or pos
    command = input("Command: ").strip()
    if command == 'dig':
        return 'dig'
    elif command == 'flag':
        return 'flag'
    else:
        command = command.split()
        if command[0].isdigit():
            x = int(command[0])
            y = int(ascii_letters.index(command[1]))
        else:
            y = int(ascii_letters.index(command[0]))
            x = int(command[1])

        if (playerboard[x-1][y] == 'F') or (x > len(playerboard)) or (y > len(playerboard)):
            print ()
            print ("INVALID INPUT")                            #checks if valid on board
            return False
        else:
            return (x-1, y)
                                                  #if empty, recursively dig surrounding
                                                  #check if empty from recursive digging
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

def flag(pboard, mboard, pos, flagged):                 #win condition if flag all bombs
    if pboard[pos[0]][pos[1]] == 'F':
        pboard[pos[0]][pos[1]]= 0
        if mboard[pos[0]][pos[1]] == '*':   
            flagged -=1
    elif pboard[pos[0]][pos[1]] == 0:
        pboard[pos[0]][pos[1]]= 'F'
        if mboard[pos[0]][pos[1]] == '*':
            flagged +=1
    return flagged

def playing(pboard):                      #lose condition if bomb appears on playerboard
    for row in range(len(pboard)):
        for column in range(len(pboard)):
            if pboard[row][column] == '*':
                return False
    return True

def setup(size, bombs):                                              #gets input for difficulty
    print ()
    print ("=======================================")
    print ()
    print ("             Minesweeper")
    print ()
    print ("=======================================")
    print ()
    print ()
    print ()
    print ("Default size: ", size)
    print ("Default bombs:", bombs)
    print ("Maximum size: 50")
    print ()
    print ("To change modes, input 'dig' or 'flag'")
    print ()
    print ("input format:", size, bombs)
    print ()
    while True:
        difficulty = input("Input board size and number of bombs: ").strip()
        if difficulty == '':
            return (size, bombs)
        try:
            difficulty = difficulty.split()
            size = int(difficulty[0])
            bombs = int(difficulty[1])
            break
        except:
            print ("invalid")
    return (size, bombs)



#Default settings
size = 15
bombs = 40
mode = 'DIG'
flagged = 0


if __name__=='__main__':                  #game loops until win or lose condition is met
    size, bombs = setup(size, bombs)
    masterboard = assign(plant_bombs(new_board(size, '-'), bombs))
    playerboard = new_board(size, 0)
    while playing(playerboard) and flagged < bombs:
        print ()
        print_board(playerboard)
        print ()
        print ("MODE: ", mode)
        print ()
        location = get_pos(playerboard)
        if location == False:
            continue
        if location == 'dig':
            mode = 'DIG'
        elif location == 'flag':
            mode = 'FLAG'
        else:
            if mode == 'DIG':
                dig(playerboard, masterboard, location)
            elif mode == 'FLAG':
                flagged = flag(playerboard, masterboard, location, flagged)

    print_board(masterboard)

    if flagged == bombs:
        print()
        print ("YOU WIN!")

    else:
        print ()
        print ("YOU DIED!")

