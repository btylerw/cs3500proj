# Beginning of file to calculate possible king moves
import chess

def kingMoves(nodePosition, grid):
    print("KING")
    checker = lambda x,y: x+y>=0 and x+y<8
    positions = []
    moves = []
    row, column = nodePosition
    currentPosition = grid[row][column]

    moves.append([-1,0])
    moves.append([1,0])
    moves.append([0,1])
    moves.append([0,-1])
    moves.append([-1,1])
    moves.append([-1,-1])
    moves.append([1,1])
    moves.append([1,-1])
    moves.append([0,3])
    moves.append([0,-4])

    for move in moves:
        RowMove, ColMove = move

        # Checks to see if piece move is valid
        if checker(RowMove, row) and checker(ColMove, column):
            # Checks to see if the space is empty for the move
            if(grid[(RowMove + row)][(ColMove + column)].piece == None):
                # Adds the move to the positions list, a list of possible positions
                positions.append((RowMove + row, ColMove + column))
            else:
                if(grid[RowMove + row][ColMove + column].piece.team == chess.opposite(grid[row][column].piece.team)):
                    # Adds the move if the piece is able to be taken
                    positions.append((RowMove + row, ColMove + column))
                elif(grid[RowMove+row][ColMove+column].piece.role == 'rook') and currentPosition.piece.first_move and\
                    grid[RowMove+row][ColMove+column].piece.first_move:
                    if ColMove > 0:
                        if grid[RowMove+row][column+1].piece == None and grid[RowMove+row][column+2].piece == None:
                            positions.append((RowMove+row, ColMove+column))
                    elif ColMove < 0:
                        if grid[RowMove+row][column-1].piece == None and grid[RowMove+row][column-2].piece == None and\
                            grid[RowMove+row][column-3].piece == None:
                            positions.append((RowMove+row, ColMove+column))


    return positions