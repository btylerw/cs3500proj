# Beginning of file to calculate possible king moves
import chess

def kingMoves(nodePosition, grid):
    print("KING")
    checker = lambda x,y: x+y>=0 and x+y<8
    positions= []
    column, row = nodePosition
    if grid[column][row].piece:
        # Vectors define all possible king moves
        vectors = [[1, -1], [1, 1], [-1, 1], [-1, -1], [0, 1], [0, -1], [1, 0], [-1, 0]]
        for vector in vectors:
            columnVector, rowVector = vector
            if checker(columnVector,column) and checker(rowVector,row):
                #grid[(column+columnVector)][(row+rowVector)].colour=ORANGE
                if not grid[(column+columnVector)][(row+rowVector)].piece:
                    positions.append((column + columnVector, row + rowVector))
                elif grid[column+columnVector][row+rowVector].piece and\
                        grid[column+columnVector][row+rowVector].piece.team==chess.opposite(grid[column][row].piece.team):
                        # Allows piece to be taken if piece is on opposite team
                        positions.append((columnVector+ column,rowVector+ row ))

    return positions