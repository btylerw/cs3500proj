# Beginning of file to calculate possible king moves
import chess

def kingMoves(nodePosition, grid):
    #print("KING")
    checker = lambda x,y: x+y>=0 and x+y<8
    positions = []
    moves = []
    row, column = nodePosition
    currentPosition = grid[row][column]

    # Adds all possible moves
    moves.append([-1,0])
    moves.append([1,0])
    moves.append([0,1])
    moves.append([0,-1])
    moves.append([-1,1])
    moves.append([-1,-1])
    moves.append([1,1])
    moves.append([1,-1])
    # These two moves are to allow castling
    if (currentPosition.piece.first_move):
        # Castling moves if White is on bottom
        if (row == 7 and currentPosition.piece.team == 'White') or (row == 0 and currentPosition.piece.team == 'Black'):
            moves.append([0,3])
            moves.append([0,-4])
        # Castling moves if Black is on bottom
        elif (row == 7 and currentPosition.piece.team == 'Black') or (row == 0 and currentPosition.piece.team == 'White'):
            moves.append([0,4])
            moves.append([0,-3])

    for move in moves:
        RowMove, ColMove = move

        # Checks to see if piece move is valid
        if checker(RowMove, row) and checker(ColMove, column):
            # Checks to see if the space is empty for the move
            if(grid[(RowMove + row)][(ColMove + column)].piece == None):
                # Adds the move to the positions list, a list of possible positions
                if ColMove >= -1 and ColMove <= 1:
                    positions.append([RowMove + row, ColMove + column])
            else:
                if(grid[RowMove + row][ColMove + column].piece.team == chess.opposite(grid[row][column].piece.team)):
                    # Adds the move if the piece is able to be taken
                    positions.append([RowMove + row, ColMove + column])
                # If the piece is a rook, we are going to check if castling is allowed
                elif(grid[RowMove+row][ColMove+column].piece.role == 'rook') and currentPosition.piece.first_move and\
                    grid[RowMove+row][ColMove+column].piece.first_move and not currentPosition.piece.checked:
                    # If that king and rook have not moved, we're going to check the direction that the castling will take place
                    match ColMove:
                        # Castles to the left if White is on bottom
                        case -4:
                            if grid[RowMove+row][column-1].piece == None and grid[RowMove+row][column-2].piece == None and\
                                grid[RowMove+row][column-3].piece == None:
                                positions.append([RowMove+row, ColMove+column])
                        # Castles to the left if Black is on bottom
                        case -3:
                            if grid[RowMove+row][column-1].piece == None and grid[RowMove+row][column-2].piece == None:
                                positions.append([RowMove+row, ColMove+column])
                        # Castles to the right if White is on bottom
                        case 3:
                                if grid[RowMove+row][column+1].piece == None and grid[RowMove+row][column+2].piece == None:
                                    positions.append([RowMove+row, ColMove+column])
                        # Castles to the right is Black is on bottom
                        case 4:                            
                            if grid[RowMove+row][column+1].piece == None and grid[RowMove+row][column+2].piece == None and\
                                grid[RowMove+row][column+3].piece == None:
                                positions.append([RowMove+row, ColMove+column])


    return positions