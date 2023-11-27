# Beginning of function to calculate possible rook moves
import chess

def rookMoves(nodePosition, grid):
    print("ROOK")
    checker = lambda x,y: x+y>=0 and x+y<8
    positions= []
    column, row = nodePosition
    if grid[column][row].piece:
        vectors = []
        for i in range(1, 8):
            vectors.append([i, 0])
            vectors.append([-i, 0])
            vectors.append([0, i])
            vectors.append([0, -i])
        for vector in vectors:
            columnVector, rowVector = vector
            if checker(columnVector,column) and checker(rowVector,row):
                #grid[(column+columnVector)][(row+rowVector)].colour=ORANGE
                if not grid[(column+columnVector)][(row+rowVector)].piece:
                    positions.append((column + columnVector, row + rowVector))
                elif grid[column+columnVector][row+rowVector].piece and\
                        grid[column+columnVector][row+rowVector].piece.team==chess.opposite(grid[column][row].piece.team):
                        positions.append((columnVector+ column,rowVector+ row ))

    return positions