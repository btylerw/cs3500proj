# Beginning of function to calculate possible pawn moves

def pawnMoves(nodePosition, grid):
    print("PAWN")
    # Call this later to check if the move is possible
    checker = lambda x,y: x+y>=0 and x+y<8
    positions = []
    column, row = nodePosition
    currentPosition = grid[column][row]

    # Setting Up to check if the piece can move two times as well as once, based on 
    # If the piece is in the starting position 
    #if grid[column][row].piece.team == 'G':
    #    if row == 1:

    # Setting Up positions grid for moves this piece can do        
    if(currentPosition.piece):
        return 
    
    return positions 


# Have this here as the function we are structuring our moves based off of 
"""
def generatePotentialMoves(nodePosition, grid):
    checker = lambda x,y: x+y>=0 and x+y<8
    positions= []
    column, row = nodePosition
    if grid[column][row].piece:
        vectors = [[1, -1], [1, 1]] if grid[column][row].piece.team == "R" else [[-1, -1], [-1, 1]]
        if grid[column][row].piece.type=='KING':
            vectors = [[1, -1], [1, 1],[-1, -1], [-1, 1]]
        for vector in vectors:
            columnVector, rowVector = vector
            if checker(columnVector,column) and checker(rowVector,row):
                #grid[(column+columnVector)][(row+rowVector)].colour=ORANGE
                if not grid[(column+columnVector)][(row+rowVector)].piece:
                    positions.append((column + columnVector, row + rowVector))
                elif grid[column+columnVector][row+rowVector].piece and\
                        grid[column+columnVector][row+rowVector].piece.team==opposite(grid[column][row].piece.team):

                    if checker((2* columnVector), column) and checker((2* rowVector), row) \
                            and not grid[(2* columnVector)+ column][(2* rowVector) + row].piece:
                        positions.append((2* columnVector+ column,2* rowVector+ row ))

    return positions
"""


