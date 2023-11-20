# Beginning of function to calculate possible pawn moves

def pawnMoves(nodePosition, grid):
    '''
    pawnMoves(nodePosition, grid) is a function that holds the possible Pawn Moves based on the chosen piece 
    within the grid. Should return a grid with a certain variable that informs a different functions what moves
    are possible.
    '''
    print("PAWN")
    # Call this later to check if the move is possible
    checker = lambda x,y: x+y>=0 and x+y<8
    moves = []
    positions = []
    column, row = nodePosition
    currentPosition = grid[column][row]

    # Setting Up to check if the piece can move two times as well as once, based on 
    # If the piece is in the starting position 
    #if grid[column][row].piece.team == 'G':
    #    if row == 1:

    # Setting Up positions grid for moves this piece can do        
    if(currentPosition.piece):
        print("Current Piece is a valid piece with a position class, it is placed at column {column} and row {row}")
    
    return positions 




