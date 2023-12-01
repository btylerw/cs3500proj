# Beginning of function to calculate possible queen moves
import chess

def queenMoves(nodePosition, grid):
    checker = lambda x,y: x+y>=0 and x+y<8
    positions = []
    moves = []
    row, column = nodePosition
    currentPosition = grid[row][column]


    distanceForward = 8 - row
    distanceBackward = 9 - distanceForward
    distanceRight = 8 - column
    distanceLeft = 9 - distanceRight
    
    #######################################
    # Horizontal And Vertical Moves
    #######################################
    # All Potential Moves Forward
    for y in range(1, distanceForward):
        if(grid[row+y][column].piece):
            if(currentPosition.piece.team == grid[row+y][column].piece.team):
                break
            else:
                moves.append([y,0])
                break
        else:
            moves.append([y,0])
    
    # All Potential Moves backwards
    for y in range(1, distanceBackward):
        if(grid[row-y][column].piece):
            if(currentPosition.piece.team == grid[row-y][column].piece.team):
                break
            else:
                moves.append([-y,0])
                break
        else:
            moves.append([-y,0])    

    # All Potential Moves Right
    for y in range(1, distanceRight):
        if(grid[row][column+y].piece):
            if(currentPosition.piece.team == grid[row][column+y].piece.team):
                break
            else:
                moves.append([0,y])
                break
        else:
            moves.append([0,y])

    # All Potential Moves left
    for y in range(1, distanceLeft):
        if(grid[row][column-y].piece):
            if(currentPosition.piece.team == grid[row][column-y].piece.team):
                break
            else:
                moves.append([0,-y])
                break
        else:
            moves.append([0,-y])

    #######################################
    # Diaganol Moves
    #######################################                                
    # All Potential Diaganol Moves Forward Right
    for y in range(1, distanceForward):
        if(checker(row, y) and checker(column, y)):
            if(grid[row+y][column+y].piece):
                if(currentPosition.piece.team == grid[row+y][column+y].piece.team):
                    break
                else:
                    moves.append([y,y])
                    break
            else:
                moves.append([y,y])
            
    # All Potential Diagnol Moves Backwards Left
    for y in range(1, distanceBackward):
        if(checker(row, -y) and checker(column, -y)):
            if(grid[row-y][column-y].piece):
                if(currentPosition.piece.team == grid[row-y][column-y].piece.team):
                    break
                else:
                    moves.append([-y,-y])
                    break
            else:
                moves.append([-y,-y])

    # All Potential Diagnol Moves Forward Left
    for y in range(1, distanceForward):
        if(checker(row, y) and checker(column, -y)):
            if(grid[row+y][column-y].piece):
                if(currentPosition.piece.team == grid[row+y][column-y].piece.team):
                    break
                else:
                    moves.append([y,-y])
                    break
            else:
                moves.append([y,-y])        

    # All Potential Diagnol Moves Backward Right
    for y in range(1, distanceBackward):
        if(checker(row, -y) and checker(column, y)):
            if(grid[row-y][column+y].piece):
                if(currentPosition.piece.team == grid[row-y][column+y].piece.team):
                    break
                else:
                    moves.append([-y,+y])
                    break
            else:
                moves.append([-y,+y])      

    for move in moves:
        RowMove, ColMove = move

        # Checks to see if piece move is valid
        if checker(RowMove, row) and checker(ColMove, column):
            # Checks to see if the space is empty for the move
            if(grid[(RowMove + row)][(ColMove + column)].piece == None):
                # Adds the move to the positions list, a list of possible positions
                positions.append([RowMove + row, ColMove + column])
            else:
                if(grid[RowMove + row][ColMove + column].piece.team == chess.opposite(grid[row][column].piece.team)):
                    # Adds the move if the piece is able to be taken
                    positions.append([RowMove + row, ColMove + column])

    return positions