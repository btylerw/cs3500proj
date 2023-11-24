# Beginning of function to calculate possible pawn moves

def pawnMoves(nodePosition, grid):
    '''
    pawnMoves(nodePosition, grid) is a function that holds the possible Pawn Moves based on the chosen piece 
    within the grid. Should return a list with the coordinates of possible moves that are possible. This function 
    typically gets called in the HighlightpotentialMoves() and resetColours() functions. Will update this docstring 
    when there is a better understanding of this this function will fit into generate moves per piece
    '''
    print("PAWN")
    # Call this later to check if the move is possible
    checker = lambda x,y: x+y>=0 and x+y<8
    moves = []
    positions = []
    column, row = nodePosition
    currentPosition = grid[column][row]
    #isFirstMove = currentPosition.getFirstMove()
    print(f"currentPosition type is {type(currentPosition)}")

    

    # Setting Up positions grid for moves this piece can do        
    if(currentPosition.piece):
        print("Current Piece is a valid piece with a position class, it is placed at column {column} and row {row}")
    
    return positions 




