from random import randint
from string import ascii_letters


def new_board(size, base):                                           #create blank board
    board = [[base for column in range(size)] for row in range(size)]
    return board

def plant_bombs(board, numbombs, bomb):                              #plant all bombs on board
    bombs = 0
    while bombs < numbombs:
        x = randint(0, len(board)-1)
        y = randint(0, len(board)-1)
        board[x][y] = bomb
        bombs += 1
    return board

def check(board, pos, bomb):                               #return number of surrounding bombs
    n = 0
    for row in range(max(0, (pos[0]-1)), min((pos[0]+2), len(board))):
        for column in range(max(0, (pos[1]-1)), min((pos[1]+2), len(board))):
            if board[row][column] == bomb:
                n += 1
    return n 

def assign(board, bomb):                          #call check function and assignment on board
    for row in range(len(board)):                   
        for column in range(len(board)):
            if board[row][column] == bomb or check(board,(row,column), bomb) == 0:
                continue
            board[row][column] = check(board,(row,column), bomb)
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

def get_pos(playerboard, flag):
    while True:                                             #input check for mode or pos
        command = input("Command: ").strip()
        if command == 'dig':                                        
            return 'dig'
        elif command == 'flag':
            return 'flag'
        else:                                            #converts input into coordinate
            try:
                x = []
                for i in (command):
                    if str(i).isdigit():
                        x.append(i)
                    if i in ascii_letters:
                        y = int(ascii_letters.index(i))

                try:
                    x = int(x[0] + x[1])
                except:
                    x = int(x[0])

                if (playerboard[x-1][y] == flag) or (x > len(playerboard)) or (y > len(playerboard)):
                    raise ValueError     #raise error if pos is flagged or out of bounds

            except:
                print ()
                print ("INVALID INPUT")
                print ()
                continue
                
            return (x-1, y)

                                                  #if empty, recursively dig surrounding
                                                  #check if empty from recursive digging
def dig(pboard, mboard, pos, empty):
    if mboard[pos[0]][pos[1]] == empty and pboard[pos[0]][pos[1]] != empty:
        pboard[pos[0]][pos[1]] = mboard[pos[0]][pos[1]]
        for row in range(max(0, (pos[0]-1)), min((pos[0]+2), len(pboard))):
            for column in range(max(0, (pos[1]-1)), min((pos[1]+2), len(pboard))):
                if pboard[row][column] == empty or (row,column) == pos:
                    continue
                elif mboard[row][column] == empty and pboard[row][column] != empty:
                    dig(pboard, mboard, (row, column), empty)          
                pboard[row][column] = mboard[row][column]
    pboard[pos[0]][pos[1]] = mboard[pos[0]][pos[1]]

def flag(pboard, mboard, pos, flagged, flag, bomb, undug):                 #win condition if flag all bombs
    if pboard[pos[0]][pos[1]] == flag:
        pboard[pos[0]][pos[1]]= undug
        if mboard[pos[0]][pos[1]] == bomb:   
            flagged -=1
    elif pboard[pos[0]][pos[1]] == undug:
        pboard[pos[0]][pos[1]]= flag
        if mboard[pos[0]][pos[1]] == bomb:
            flagged +=1
    return flagged

def playing(pboard, bomb):                      #lose condition if bomb appears on playerboard
    for row in range(len(pboard)):
        for column in range(len(pboard)):
            if pboard[row][column] == bomb:
                return False
    return True

def setup(size, bombs):                                       #gets input for difficulty
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
empty_sym = chr(11038)  # '-'
undug_sym = chr(9642)   #  0
bomb_sym = chr(10694)   # '*'
flag_sym = chr(10692)   # 'F'

if __name__=='__main__':                  #game loops until win or lose condition is met
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
        flagged = 0
        mode = 'DIG'
        size, bombs = setup(size, bombs)
        masterboard = assign(plant_bombs(new_board(size, empty_sym), bombs, bomb_sym), bomb_sym)
        playerboard = new_board(size, undug_sym)
        while playing(playerboard, bomb_sym) and flagged < bombs:
            print ()
            print_board(playerboard)
            print ()
            print ("MODE: ", mode)
            print ()
            location = get_pos(playerboard, flag_sym)
            if location == 'dig':
                mode = 'DIG'
            elif location == 'flag':
                mode = 'FLAG'
            else:
                if mode == 'DIG':
                    dig(playerboard, masterboard, location, empty_sym)
                elif mode == 'FLAG':
                    flagged = flag(playerboard, masterboard, location, flagged, flag_sym, bomb_sym, undug_sym)
    
        print_board(masterboard)
    
        if flagged == bombs:
            print ()
            print ("YOU WIN!")
    
        else:
            print ()
            print ("YOU DIED!")
        
        print ()
        print ("Bombs flagged:", flagged, "out of", bombs)
        print ()
        choice = input ("Do you want to play again? (yes/no) ").lower().strip()
        if choice == 'no':
            print ()
            print ("Thank you for playing!")
            input ()
            break
        else:
            continue

    

