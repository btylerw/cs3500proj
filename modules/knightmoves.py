# Beginning of function to calculate possible knight moves
import chess

def knightMoves(nodePosition, grid, targeting):
    # Call this later to check if the move is possible
    checker = lambda x,y: x+y>=0 and x+y<8
    moves = [[-2, 1], [-2, -1], [2, 1], [2, -1], [-1, -2], [-1, 2], [1, -2], [1, 2]]
    positions = []
    row, column = nodePosition
    currentPosition = grid[row][column]

    if currentPosition.piece:
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
                    if targeting:
                        positions.append([RowMove + row, ColMove + column])

    return positions 