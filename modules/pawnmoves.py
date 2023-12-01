# Beginning of function to calculate possible pawn moves
import chess 

def pawnMoves(nodePosition, grid):
    '''
    pawnMoves(nodePosition, grid) is a function that holds the possible Pawn Moves based on the chosen piece 
    within the grid. Should return a list with the coordinates of possible moves that are possible. This function 
    typically gets called in the HighlightpotentialMoves() and resetColours() functions. Will update this docstring 
    when there is a better understanding of this this function will fit into generate moves per piece
    '''
    # Call this later to check if the move is possible
    checker = lambda x,y: x+y>=0 and x+y<8
    moves = []
    positions = []
    row, column = nodePosition
    currentPosition = grid[row][column]

    # Setting Up positions grid for moves this piece can do        
    if(currentPosition.piece):
        # Assigns moves based on team and if it's the piece's first move
        match currentPosition.piece.team:
            case 'Black':
                # Checks to see if the position in front is empty 
                if(grid[row+1][column].piece == None):
                    if(currentPosition.piece.first_move) and (grid[row+2][column].piece == None): moves = [[1,0],[2,0]]
                    else: moves = [[1,0]]

                # Checks if a piece is able to be taken
                if(checker(row, 1) and checker(column, 1)):
                    if(grid[row+1][column+1].piece != None):
                        if(grid[row+1][column+1].piece.team == 'White'):
                            moves.append([1,1])

                if(checker(row, 1) and checker(column, -1)):
                    if(grid[row+1][column-1].piece != None):
                        if(grid[row+1][column-1].piece.team == 'White'):
                            moves.append([1,-1])                
                               
            case 'White':
                # Checks to see if the position in front is empty 
                if(grid[row-1][column].piece == None):
                    if(currentPosition.piece.first_move) and (grid[row-2][column].piece == None): moves = [[-1,0],[-2,0]]
                    else: moves = [[-1,0]]

                # Checks if a piece is able to be taken
                if(checker(row, -1) and checker(column, 1)):
                    if(grid[row-1][column+1].piece != None):
                        if(grid[row-1][column+1].piece.team == 'Black'):
                            moves.append([-1,1])

                if(checker(row, -1) and checker(column, -1)):
                    if(grid[row-1][column-1].piece != None):
                        if(grid[row-1][column-1].piece.team == 'Black'):
                            moves.append([-1,-1])

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




