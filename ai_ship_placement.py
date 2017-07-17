def get_AI_ships(width, height, board, file):
    ship_lines = []     
    for ship_line in file:     
        ship_line = ship_line.split()
        ship_lines.append(ship_line)
    ship_lines = sorted(ship_lines)
    for line in ship_lines:
        marker = line[0]
        row1 = int(line[1])
        column1 = int(line[2])
        row2 = int(line[3])
        column2 = int(line[4])
        if row1 > row2:
            smaller_r = row2
            row2 = row1
            row1 = smaller_r
        elif column1 > column2:
            smaller_c = column2
            column2 = column1
            column1 = smaller_c
        if row1 == row2 and column1 == column2:
            ship_length = 1
        elif row2 - row1 == 0:
            ship_length = column2 - column1 + 1
        elif column2 - column1 == 0:
            ship_length = (row2 - row1) + 1
            
        valid = False
        while valid == False:
            choice = random.choice(['vert', 'horz'])   
            if choice == 'vert':
                row = random.randint(0, (height - ship_length))   
                ship_row = int(row)
                column = random.randint(0, (width - 1))
                for ship_part in range(ship_length):
                    if board[ship_row][column] != '*':
                        break
                    ship_row += 1
                else:
                    for ship_part2 in range(ship_length):
                        board[row+ship_part2][column] = marker
                    else:   
                        print('Placing ship from %d,%d to %d,%d.' %(row,column,((row+ship_length-1)),column))
                        valid = True
            elif choice == 'horz':
                row = random.randint(0, height - 1)   
                column = random.randint(0, (width - ship_length))
                ship_column = int(column)
                for ship_part3 in range(ship_length):
                    if board[row][ship_column] != '*':
                        break
                    ship_column += 1
                else:
                    for ship_part4 in range(ship_length):
                        board[row][column+ship_part4] = marker
                    else:
                        print('Placing ship from %d,%d to %d,%d.' %(row,column,row,((column+ship_length)-1)))
                        valid = True
    return board 
