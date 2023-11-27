# Beginning of function to calculate possible knight moves
import chess

def knightMoves(nodePosition, grid):
    print("KNIGHT")
    checker = lambda x,y: x+y>=0 and x+y<8
    positions= []
    column, row = nodePosition
    if grid[column][row].piece:
        # Vectors for all legal knight moves
        vectors = [[-2, 1], [-2, -1], [2, 1], [2, -1], [-1, -2], [-1, 2], [1, -2], [1, 2]] 
        for vector in vectors:
            # TODO: change up logic here to make knight function appropriately
            # Currently some legal moves can be made, but has many bugs
            columnVector, rowVector = vector
            if checker(columnVector,column) and checker(rowVector,row):
                #grid[(column+columnVector)][(row+rowVector)].colour=ORANGE
                if not grid[(column+columnVector)][(row+rowVector)].piece:
                    positions.append((column + columnVector, row + rowVector))
                elif grid[column+columnVector][row+rowVector].piece and\
                        grid[column+columnVector][row+rowVector].piece.team==chess.opposite(grid[column][row].piece.team):
                        
                        positions.append((column+columnVector, row+rowVector))

    return positions