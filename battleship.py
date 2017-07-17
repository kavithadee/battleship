#play the game battleship

import random
import sys

def make_board(width,height):
  """
  create a battleship board. It is represented as a list of lists
  with each inner list containing the elements in a row. The blank spaces
  are represented with *. A battleship board is width X height
  @returns: a battleship board.
  """
  board = []
  for row_index in range(height): #for each row in the board
    row = ['*'] * width #it should be empty and width wide
    board.append(row) #add in the row
  return board

def display_board(board):
  """
  display the given board.
  @board: a list of lists of characters.
  @returns: None
  """

  print(' ', end = '') #display some white space for alignment purposes
  #display the column headers
  for col_num in range(len(board[0])):
    print('', col_num, end = '')
  print()

  for (row_num,row) in enumerate(board): #for each row
    print(row_num, ' '.join(row)) #print out the row header and each element


def moves(contents,width,height):
    ships={}
    count_dict={}
    ship_len=[]
    ship_values=[]
    for line in contents:
        values=[]
        moves_list=line.split()
        symbol=moves_list[0]

        if symbol in count_dict: #check to make sure symbols are unique
            count_dict[symbol]+=1
        else:
            count_dict[symbol]=1

        if count_dict[symbol]>1: #if symbol appears more than once then symbol is not unique
            print("Error symbol %s is already in use. Terminating game"%symbol)
            sys.exit(0)

        symbol=valid_symbol(symbol)
        row1_index=valid_index(moves_list[1],height,symbol)
        col1_index=valid_index(moves_list[2],width,symbol)
        row2_index=valid_index(moves_list[3],height,symbol)
        col2_index=valid_index(moves_list[4],width,symbol)

        if (row1_index!=row2_index) and (col1_index!=col2_index): #checks to make sure ship is not placed diagonally
            print ("Ships cannot be placed diagonally. Terminating game.")
            sys.exit(0)

        #get coordinates of placements of ships
        if row1_index==row2_index: #ship is placed horizontally
            if col2_index>col1_index:
                ship_len.append(col2_index-col1_index+1)
                i=col1_index
                while i<=col2_index:
                    values.append((row1_index,i)) #updates values of all coordinates of each ship
                    ship_values.append((row1_index,i)) #updates values of all coordinates of all ships
                    i+=1
            else:
                ship_len.append(col1_index-col2_index+1)
                i=col2_index
                while i<=col1_index:
                    values.append((row1_index,i))
                    ship_values.append((row1_index,i))
                    i+=1
        else: #ship is placed vertically
            if row2_index>row1_index:
                ship_len.append(row2_index-row1_index+1)
                i=row1_index
                while i<=row2_index:
                    values.append((i,col1_index))
                    ship_values.append((i,col1_index))
                    i+=1
            else:
                ship_len.append(row1_index-row2_index+1)
                i=row2_index
                while i<=row1_index:
                    values.append((i,col1_index))
                    ship_values.append((i,col1_index))
                    i+=1

        for i in range(len(ship_values)): #checks to make sure ships are not overlapping
          for j in range(i+1, len(ship_values)):
            if ship_values[i] == ship_values[j]:
              print("There is already a ship at location %d, %d. Terminating game." % (ship_values[i][0], ship_values[i][1]))
              sys.exit(0)
              
        ships[symbol]=values #creates dictionary with keys as ship names and values as list of coordinates of ship on board in the form of tuples

    return (ships,ship_len) #returns dictionary of users ships and list of length of each ship

def place_ships_user(board,ships): #places users ships on board and returns board
    for key,val in ships.items():
        for tup in val:
            row,col=tup
            board[row][col]=key
    return board


def AI_ship(width, height, board, file): #places AI's ships on board and returns board and dictionary of AI's ships
    AI_ships={}
    ship_line = []     
    for ship_lines in file: #for line in content of files
        ship_lines = ship_lines.split() #split line to get symbol and coordinates
        ship_line.append(ship_lines)
    ship_line = sorted(ship_line) #places ships in alphabetic order
    for line in ship_line:
        values=[] #list of coordinates of each ship
        symbol = line[0]
        row1 = int(line[1])
        column1 = int(line[2])
        row2 = int(line[3])
        column2 = int(line[4])
        if row1 > row2: #get smaller and larger values to calculate ship length
            smaller_r = row2
            row2 = row1
            row1 = smaller_r
        elif column1 > column2: #get smaller and larger values to calculate ship length
            smaller_c = column2
            column2 = column1
            column1 = smaller_c
        if row1 == row2 and column1 == column2:
            ship_length = 1
        elif row2 - row1 == 0:
            ship_length = column2 - column1 + 1
        elif column2 - column1 == 0:
            ship_length = (row2 - row1) + 1
            
        valid = True
        while valid:
            choice = random.choice(['vert', 'horz']) #randomly choose orientation of ship
            if choice == 'vert':
                row = random.randint(0, (height - ship_length))   
                ship_row = int(row)
                column = random.randint(0, (width - 1))
                for ship_part in range(ship_length):
                    if board[ship_row][column] != '*': #ship must be placed in empty spot
                        break
                    ship_row += 1
                else:
                    for ship_part2 in range(ship_length):
                        board[row+ship_part2][column] = symbol #if spot is empty, ship is placed
                        values.append((row+ship_part2,column)) #spot added to list of values
                    else:   
                        print('Placing ship from %d,%d to %d,%d.' %(row,column,((row+ship_length-1)),column))
                        valid = False
            elif choice == 'horz':
                row = random.randint(0, height - 1)   
                column = random.randint(0, (width - ship_length))
                ship_column = int(column)
                for ship_part3 in range(ship_length):
                    if board[row][ship_column] != '*': #ship must be placed in empty spot
                        break
                    ship_column += 1
                else:
                    for ship_part4 in range(ship_length):
                        board[row][column+ship_part4] = symbol #if spot is empty, ship is placed
                        values.append((row,column+ship_part4)) #spot added to list of values
                    else:
                        print('Placing ship from %d,%d to %d,%d.' %(row,column,row,((column+ship_length)-1)))
                        valid = False
        AI_ships[symbol]=values #dictionary formed with ship symbol as keys and list of coordinates as values
    return (AI_ships,board) 

def is_valid_int(integer):
  """
  checks to see if number represents a valid integer
  @number: a string that might represent an integer
  @returns: true if the string represents an integer
  """
  integer = integer.strip()
  if len(integer) == 0:
    return False
  else:
    return (integer.isdigit() or #only digits
            #or a negative sign followed by digits
            (integer.startswith('-') and integer[1:].isdigit()))


def is_valid_move_user(str_move, board, width, height):
  """
  check if the move is valid on the given board
  @str_move: the potential move. should be row column
  @board: a list of lists of characters.
  @returns: True if the move is valid and False otherswise
  """
  str_move = str_move.split() #break it up into row and col

  if len(str_move) != 2:
    return False

  (row,col) = str_move #get row row and column

  if not is_valid_int(row):#row isn't a number
    return False

  if not is_valid_int(col):#column isn't a number
    return False

  #safe to convert to integers
  row = int(row)
  col = int(col)

  if row not in range(height) or col not in range(width): #move needs to be on the board
    return False

  if board[row][col]=='X' or board[row][col]=='O': #we can't play at a place that's already been played
    return False

  return True #move wasn't illegal so it must be legal

def get_move_user(board,width,height):
  """
  get a valid move from the player
  @player: a string representing the current player
  @board: the board
  @returns: a valid move, which is a the following tuple (row, col)
  """

  move = '' #make the move start as wrong so that we always go into the while loop
  while not is_valid_move_user(move, board,width,height): #while the input is invalid
    move = input('Enter row and column to fire on separated by a space: ') #keep asking for input

  (row, col) = move.split() #break apart

  #turn to integers
  row = int(row)
  col = int(col)
  return (row, col)


def make_move(row,col,board1,board2):

    if board1[row][col]=='*': #if empty spot, miss
        board2[row][col]='O' #update displayed board
        return ("Miss!",board2)
    elif board1[row][col]!='X' and board1[row][col]!='O': #if not empty spot and not hit or miss, is hit
        board2[row][col]='X'
        return ("Hit!",board2)



def sink_ship(values,board): #checks if ship is sunken
    i=0
    for spot in values:
        if board[spot[0]][spot[1]]=="X": #if each coordinate of ship is a hit, ship is sunken
            i+=1
        else:
            return False
    if i==len(values):
        return True
    else:
        return False

def isgameover(ships,board): #checks if gqme is over by checking if all ships are sunken
    i=0
    for key,values in ships.items(): 
        if sink_ship(values,board): #checks if each ship in dictionary is sunken
            i+=1
            continue
        else:
            return False
    if i==len(ships): #game is over
        return True
    else:
        return False

def random_AI(board,width,height): #returns coordinate from list of empty spots
    empty_spots=[]
    for row in range(height):
        for col in range(width):
            if board[row][col]!='X' and board[row][col]!='O': #if spot is not a hit or miss, move on that spot has not been made
                empty_spots.append((row,col))
    if len(empty_spots)==0: 
        pass
    else:
        r,c=random.choice(empty_spots) #choose random coordinate from list of empty spots
        return (r,c)

def emptyspots(board,width,height): #returns coordinate from list of empty spots
    empty_spots=[]
    for row in range(height):
        for col in range(width):
            if board[row][col]!='X' and board[row][col]!='O': #if spot is not a hit or miss, move on that spot has not been made
                empty_spots.append((row,col))
    if len(empty_spots)==0:
        pass
    else:
       return empty_spots

def valid_seed(num):
    while not (num.isdigit() or #only digits
            #or a negative sign followed by digits
            (num.startswith('-') and num[1:].isdigit())):
        num=input("Enter the seed: ")
    return int(num)

def valid_width(num):
    while not (num.isdigit() and int(num)>0): #width is a number and is positive
        num=input("Enter the width of the board: ")
    num=int(num)
    return num

def valid_height(num):
    while not (num.isdigit() and int(num)>0): #height is a number and positive
        num=input("Enter the height of the board: ")
    num=int(num)
    return num

def valid_symbol(sym):
    while not(sym!='x' and sym!='X' and sym!='o' and sym!='O' and sym!='*'): #symbol is not any special character used in game
        print ("Invalid symbol. Terminating game.")
        sys.exit(0)
    return sym

def valid_index(ind,bound,symbol):
    while not(int(ind)<bound and int(ind)>=0): #index is on board and positive
        print ("Error %s is placed outside of the board. Terminating game."%symbol)
        sys.exit(0)
    return int(ind)

def AI_choice(): #gets input choice from user and validates it
    print ("Choose your AI.")
    print ("1. Random\n2. Smart\n3. Cheater")
    choice=input("Your choice: ")
    while not(choice.isdigit() and int(choice)>=1 and int(choice)<=3): #choice is a number and either 1, 2 or 3
        print ("Choose your AI.")
        print ("1. Random\n2. Smart\n3. Cheater")
        choice=input("Your choice: ")
    return int(choice)

def play_battleship(): #gameplay
    seed_val=input("Enter the seed: ")
    seed_val=valid_seed(seed_val)
    random.seed(seed_val) #seeds number

    width=input("Enter the width of the board: ")
    width=valid_width(width) #gets width value

    height=input("Enter the height of the board: ")
    height=valid_height(height) #gets height value

    file_name=input("Enter the name of the file containing your ship placements: ")
    f=open(file_name) #opens file name
    f_content=f.readlines() #gets list of lines in file 

    choice=AI_choice() #gets choice value

    ships,ship_len=moves(f_content,width,height) #gets dictionary of user's ships and list of lengths of users ships
    
    user_board=place_ships_user(make_board(width,height),ships) #places ships on user's board
    user_moves=make_board(width,height) #makes board to display user's moves
    AI_ships,AI_board=AI_ship(width,height,make_board(width,height),f_content) #gets dictionary of AI's ships and places ships on AI's boards
    AI_moves=make_board(width,height) #makes board with AI's moves

    turn=random.randint(0,1) #turn randomly chosen
    if choice==1: #if random AI
        valid=True
        while valid:
            if turn==0: #user's move
                print ("Scanning Board")
                display_board(user_moves)
                print ("\nMy Board")
                display_board(user_board)
                row,col=get_move_user(user_moves,width,height) 
                result,user_moves=make_move(row,col,AI_board,user_moves)


                if result=='Hit!': #if hit updates board and checks for ship sink
                    key=AI_board[row][col]
                    AI_board[row][col]='X'
                    if sink_ship(AI_ships[key],AI_board):
                            print ("You sunk my",key)
                    else:
                      print (result)

                else: #miss
                    print (result) 
                    AI_board[row][col]='O'
                valid=not(isgameover(ships,user_board) or isgameover(AI_ships,AI_board)) #checks if game is over 
                if valid==False: #breaks if game is over
                  break
                turn=1 #changes turn

            if turn==1: #AI's moves
                    r,c=random_AI(user_board,width,height) 
                    print ("The AI fires at location (%d, %d)"%(r,c))
                    result,AI_moves=make_move(r,c,user_board,AI_moves)

                    if result=='Hit!':
                        key=user_board[r][c]
                        user_board[r][c]='X'
                        if sink_ship(ships[key],user_board):
                            print ("You sunk my",key)
                        else:
                          print (result)
                    else:
                        print (result)
                        user_board[r][c]='O'
                    valid=not(isgameover(ships,user_board) or isgameover(AI_ships,AI_board))
                    if valid==False:
                        break
                    turn=0

        if turn==0:
            print ("Scanning Board")
            display_board(user_moves)
            print ("\nMy Board")
            display_board(user_board)
            print ("\nYou win!")

        else:
            print ("Scanning Board")
            display_board(user_moves)
            print ("\nMy Board")
            display_board(user_board)
            print ("\nThe AI wins.")

    elif choice==3: #cheating AI
        is_ship=[] 
        for r in range(0,len(user_board)):
            for c in range(0,len(user_board[r])):
                if user_board[r][c]!='*':
                    is_ship.append((r,c)) #gets list of coordinates of ship places row by row
                else:
                    continue
        for move in is_ship: #iterates through list of coordinates of ship placements
            r,c=move
            valid=True
            while valid:
                if turn==0: #user's move
                    print ("Scanning Board")
                    display_board(user_moves)
                    print ("\nMy Board")
                    display_board(user_board)
                    row,col=get_move_user(user_moves,width,height)
                    result,user_moves=make_move(row,col,AI_board,user_moves)


                    if result=='Hit!':
                        key=AI_board[row][col]
                        AI_board[row][col]='X'
                        if sink_ship(AI_ships[key],AI_board):
                                print ("You sunk my",key)
                        else:
                          print (result)

                    else:
                        print (result)
                        AI_board[row][col]='O'
                    valid=not(isgameover(ships,user_board) or isgameover(AI_ships,AI_board))
                    turn=1
                    if valid==False:
                      break
                    

                if turn==1: #Ai's move
                    print ("The AI fires at location (%d, %d)"%(r,c))
                    result,AI_moves=make_move(r,c,user_board,AI_moves)

                    if result=='Hit!':
                        key=user_board[r][c]
                        user_board[r][c]='X'
                        if sink_ship(ships[key],user_board):
                            print ("You sunk my",key)
                        else:
                          print (result)
                    else:
                        print (result)
                        user_board[r][c]='O'
                    valid=not(isgameover(ships,user_board) or isgameover(AI_ships,AI_board))
                    turn=0
                    break
                    
                if valid==False:
                    break
                else:
                    continue
        if turn==1:
            print ("Scanning Board")
            display_board(user_moves)
            print ("\nMy Board")
            display_board(user_board)
            print ("\nYou win!")

        else:
            print ("Scanning Board")
            display_board(user_moves)
            print ("\nMy Board")
            display_board(user_board)
            print ("\nThe AI wins.")

    elif choice==2: #smart AI
        destroy=[] #list of potential turns
        random_moves=emptyspots(user_board,width,height)
        valid=True
        while valid:
            if turn==0: #user's move
                print ("Scanning Board")
                display_board(user_moves)
                print ("\nMy Board")
                display_board(user_board)
                row,col=get_move_user(user_moves,width,height)
                result,user_moves=make_move(row,col,AI_board,user_moves)


                if result=='Hit!':
                    key=AI_board[row][col]
                    AI_board[row][col]='X'
                    if sink_ship(AI_ships[key],AI_board):
                            print ("You sunk my",key)
                    else:
                      print (result)

                else:
                    print (result)
                    AI_board[row][col]='O'
                valid=not(isgameover(ships,user_board) or isgameover(AI_ships,AI_board))
                if valid==False:
                  break
                else:
                    turn=1
                
            if turn==1: #AI's turn
                length=len(destroy)
                if length == 0: #if there are no moves in list, then randomly choose the AI's move
                    move = random.choice(random_moves)
                    print('The AI fires at location', move)
                    index = random_moves.index(move) #finds index of move in list of random moves
                    random_moves.pop(index) #removes move from list
                    result,AI_moves=make_move(move[0],move[1],user_board,AI_moves) #checks if AI move hit a player ship
                    if result == "Hit!":
                        key=user_board[move[0]][move[1]]
                        user_board[move[0]][move[1]]='X'
                        if sink_ship(ships[key],user_board):
                            print ("You sunk my",key)
                        else:
                            print (result)
                        (row, col) = move #gets potential spots if move is a hit
                        above = row - 1
                        below = row + 1
                        left = col - 1
                        right = col + 1

                        if above in range(height): #gets spot above
                            move = (above, col)
                            if random_moves.count(move) == 1 and destroy.count(move) == 0: #if move is in list of random move, added to list of potential smart spots
                                destroy.append(move)

                        if below in range(height): #gets spot below
                            move = (below, col)

                            if random_moves.count(move) == 1 and destroy.count(move) == 0: #if move is in list of random move, added to list of potential smart spots
                                destroy.append(move)

                        if left in range(width): #gets spot to the left
                            move = (row, left)

                            if random_moves.count(move) == 1 and destroy.count(move) == 0: #if move is in list of random move, added to list of potential smart spots
                                destroy.append(move)

                        if right in range(width): #gets spot to the right
                            move = (row, right)

                            if random_moves.count(move) == 1 and destroy.count(move) == 0: #if move is in list of random move, added to list of potential smart spots
                                destroy.append(move)
                    else:
                        print (result)
                        user_board[move[0]][move[1]]='O'
                    valid=not(isgameover(ships,user_board) or isgameover(AI_ships,AI_board))
                    if valid==False:
                      break
                    else:
                      turn=0
                
                else:
                    move = destroy[0]
                    print('The AI fires at location', move)
                    index = random_moves.index(move)
                    destroy.pop(0)
                    random_moves.pop(index)
                    result,AI_moves=make_move(move[0],move[1],user_board,AI_moves) #checks if AI move hit a player ship

                    if result == "Hit!":
                        key=user_board[move[0]][move[1]]
                        user_board[move[0]][move[1]]='X'
                        if sink_ship(ships[key],user_board):
                            print ("You sunk my",key)
                        else:
                            print (result)
                        (row, col) = move
                        above = row - 1
                        below = row + 1
                        left = col - 1
                        right = col + 1

                        if above in range(height): #gets spot above
                            move = (above, col)
                            if random_moves.count(move) == 1 and destroy.count(move) == 0: #if move is in list of random move, added to list of potential smart spots
                                destroy.append(move)

                        if below in range(height): #gets spot below
                            move = (below, col)
                            if random_moves.count(move) == 1 and destroy.count(move) == 0: #if move is in list of random move, added to list of potential smart spots
                                destroy.append(move)

                        if left in range(width): #gets spot to the left
                            move = (row, left)
                            if random_moves.count(move) == 1 and destroy.count(move) == 0: #if move is in list of random move, added to list of potential smart spots
                                destroy.append(move)

                        if right in range(width): #gets spot to the right
                            move = (row, right)
                            if random_moves.count(move) == 1 and destroy.count(move) == 0: #if move is in list of random move, added to list of potential smart spots
                                destroy.append(move)
                    else:
                        print (result)
                        user_board[move[0]][move[1]]='O'
                    valid=not(isgameover(ships,user_board) or isgameover(AI_ships,AI_board))
                    if valid==False:
                      break
                    turn=0

            
        if turn==0:
            print ("Scanning Board")
            display_board(user_moves)
            print ("\nMy Board")
            display_board(user_board)
            print ("\nYou win!")

        else:
            print ("Scanning Board")
            display_board(user_moves)
            print ("\nMy Board")
            display_board(user_board)
            print ("\nThe AI wins.")
        

play_battleship()

