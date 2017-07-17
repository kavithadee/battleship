def SmartAI(destroy, Random_options, game_board, board_coordinate, coor, width, height): #AI that will run smart mode, and guess around hits
    if len(destroy) == 0: #if there are no moves in list, then randomly choose the AI's move
        move = random.choice(Random_options)
        print('The AI fires at location', move)
        index = Random_options.index(move)
        Random_options.pop(index)
        decision = make_AImove(move, game_board, board_coordinate, coor, width, height) #checks if AI move hit a player ship
        if decision == True: 
            (row, col) = move
            up = row - 1
            down = row + 1
            left = col - 1
            right = col + 1
            
            if up in range(height): 
                move = (up, col)
                if Random_options.count(move) == 1 and destroy.count(move) == 0:
                    destroy.append(move)
                    
            if down in range(height):
                move = (down, col)
                
                if Random_options.count(move) == 1 and destroy.count(move) == 0:
                    destroy.append(move)
                    
            if left in range(width):
                move = (row, left)
                
                if Random_options.count(move) == 1 and destroy.count(move) == 0:
                    destroy.append(move)
                    
            if right in range(width):
                move = (row, right)
                
                if Random_options.count(move) == 1 and destroy.count(move) == 0:
                    destroy.append(move)
                    
    elif len(destroy) != 0: #if there are moves in the destroy list, those moves will be made first before choosing randomly again
        move = destroy[0]
        print('The AI fires at location', move)
        index = Random_options.index(move)
        destroy.pop(0)
        Random_options.pop(index)
        decision = make_AImove(move, game_board, board_coordinate, coor, width, height) #checks if AI move hit a player ship

        if decision == True:
            (row, col) = move
            up = row - 1
            down = row + 1
            left = col - 1
            right = col + 1

            if up in range(height):
                move = (up, col)
                if Random_options.count(move) == 1 and destroy.count(move) == 0:
                    destroy.append(move)
                    
            if down in range(height):
                move = (down, col)
                if Random_options.count(move) == 1 and destroy.count(move) == 0:
                    destroy.append(move)
                    
            if left in range(width):
                move = (row, left)
                if Random_options.count(move) == 1 and destroy.count(move) == 0:
                    destroy.append(move)
                    
            if right in range(width):
                move = (row, right)
                if Random_options.count(move) == 1 and destroy.count(move) == 0:
                    destroy.append(move)
