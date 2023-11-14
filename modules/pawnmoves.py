# Beginning of function to calculate possible pawn moves

def pawnMoves(nodePosition, grid):
    print("PAWN")
    positions = []
    column, row = nodePosition

    # Setting Up to check if the piece can move two times as well as once, based on 
    # If the piece is in the starting position 
    #if grid[column][row].piece.team == 'G':
    #    if row == 1:

    # Setting Up positions grid for moves this piece can do        
    if grid[column][row].piece:
        moves = [[0,1]]

    

