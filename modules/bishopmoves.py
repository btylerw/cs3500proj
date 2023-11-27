# Beginning of function to calculate possible bishop moves
import chess

def bishopMoves(nodePosition, grid):
    print("BISHOP")
    checker = lambda x,y: x+y>=0 and x+y<8
    positions= []
    column, row = nodePosition
    if grid[column][row].piece:
        vectors = []
        # Adds all possible moves for bishop into vector list
        for i in range(1,8):
            vectors.append([i, i])
            vectors.append([-i, i])
            vectors.append([i,-i])
            vectors.append([-i,-i])
        for vector in vectors:
            columnVector, rowVector = vector
            # TODO: Add functionality to not allow piece to move past another piece in it's way
            if checker(columnVector,column) and checker(rowVector,row):
                #grid[(column+columnVector)][(row+rowVector)].colour=ORANGE
                if not grid[(column+columnVector)][(row+rowVector)].piece:
                    positions.append((column + columnVector, row + rowVector))
                elif grid[column+columnVector][row+rowVector].piece and\
                        grid[column+columnVector][row+rowVector].piece.team==chess.opposite(grid[column][row].piece.team):
                        # Allows piece to be taken if it is on the opposite team
                        positions.append((column+columnVector, row+rowVector))

    return positions