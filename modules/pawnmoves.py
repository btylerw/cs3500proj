# Beginning of function to calculate possible pawn moves

def pawnMoves(nodePosition, grid):
    '''
    pawnMoves(nodePosition, grid) is a function that holds the possible Pawn Moves based on the chosen piece 
    within the grid. Should return a grid with a certain variable that informs a different functions what moves
    are possible. The way this function is used in the checkers.py file is it calls the move for each piece when it
    is clicked, and the function returns a grid with the possible moves. This function typically gets called in the
    HighlightpotentialMoves() and resetColours() functions. Will update this docstring when there is a better understanding
    of this this function will fit into generate moves per piece
    '''
    print("PAWN")
    # Call this later to check if the move is possible
    checker = lambda x,y: x+y>=0 and x+y<8
    moves = []
    positions = []
    column, row = nodePosition
    currentPosition = grid[column][row]
    isFirstMove = currentPosition.getFirstMove()

    # Setting Up to check if the piece can move two times as well as once, based on 
    # If the piece is in the starting position 
    #if grid[column][row].piece.team == 'G':
    #    if row == 1:

    # Setting Up positions grid for moves this piece can do        
    if(currentPosition.piece):
        print("Current Piece is a valid piece with a position class, it is placed at column {column} and row {row}")
    
    return positions 




