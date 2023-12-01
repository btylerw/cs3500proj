########################################################m
# CMPS 3500 - Class Project
# Checkers game simulator
# This is a program that will simulate a checkers board
# and provide basic game functionalities.
# This program does not abide all the rules of checkers
########################################################

import pygame
import random
import sys
from itertools import combinations
import os

from modules.pawnmoves import pawnMoves
from modules.rookmoves import rookMoves
from modules.knightmoves import knightMoves
from modules.bishopmoves import bishopMoves
from modules.queenmoves import queenMoves
from modules.kingmoves import kingMoves


# current directory
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'relative/path/to/file/you/want')


WIDTH = 800
ROWS = 8


BPAWN= pygame.image.load(os.path.join(dirname, 'images/blackpawn.png'))
BROOK= pygame.image.load(os.path.join(dirname, 'images/blackrook.png'))
BKNIGHT = pygame.image.load(os.path.join(dirname, 'images/blackknight.png'))
BBISHOP = pygame.image.load(os.path.join(dirname, 'images/blackbishop.png'))
BQUEEN = pygame.image.load(os.path.join(dirname, 'images/blackqueen.png'))
BKING = pygame.image.load(os.path.join(dirname, 'images/blackking.png'))

WPAWN= pygame.image.load(os.path.join(dirname, 'images/whitepawn.png'))
WROOK= pygame.image.load(os.path.join(dirname, 'images/whiterook.png'))
WKNIGHT = pygame.image.load(os.path.join(dirname, 'images/whiteknight.png'))
WBISHOP = pygame.image.load(os.path.join(dirname, 'images/whitebishop.png'))
WQUEEN = pygame.image.load(os.path.join(dirname, 'images/whitequeen.png'))
WKING = pygame.image.load(os.path.join(dirname, 'images/whiteking.png'))

#NOT BEING USED YET
REDKING = pygame.image.load(os.path.join(dirname, 'images/redking.png'))
GREENKING = pygame.image.load(os.path.join(dirname, 'images/greenking.png'))


WHITE = (255,255,255)
BLACK = (130,200,52)
#BLACK = (0, 0, 0)
ORANGE = (235, 168, 52)
BLUE = (76, 252, 241)
RED = (255, 0, 0)


pygame.init()
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption('Chess')

# Targeted is a dictionary that is going to store possible moves for every piece so the king can see 
# spots that they are not able to move to 
def updateTargeted(grid):
    '''
    updateTargeted(grid) is used to update our targeted dictionary. This dictionary is used to store the most current moves every 
    piece is able to do on their next turn. The point of storing this, is so our king can refer to this for moves they are not 
    allowed to move too

    Parameters:
    - grid: The grid that stores all the current pieces 
    '''
    checker = lambda x,y: x+y>=0 and x+y<8
    targeted = {}
    for row in range(len(grid)):
        for column in range(len(grid)):
            nodePosition = row, column
            positions = []
            
            if(grid[row][column].piece):
                # Storing keys as Team + "_" + Role format i.e. Black_rook or White_knight
                theKey = (grid[row][column].piece.team + "_" + grid[row][column].piece.role)
                match grid[row][column].piece.role:
                    case 'pawn': 
                        # Changing positions to hold moves the pawn can take, since their forward moves aren't the pieces they 
                        # can take. Grabs diaganol. Also checking to see if there is already a repeat of this piece, and if 
                        # so to append the moves since its two diff pieces of the same team  
                        if(grid[row][column].piece.team == 'White'):
                            if(checker(row, -1) and checker(column, 1)):
                                if theKey in targeted: targeted[theKey].append([row-1, column+1])
                                else: positions.append([row-1, column+1])
                            
                            if(checker(row, -1) and checker(column, -1)):
                                if theKey in targeted: targeted[theKey].append([(row-1), (column-1)])                                    
                                else: positions.append([row-1, column-1])
                        else:
                            if(checker(row, 1) and checker(column, 1)):
                                if theKey in targeted: targeted[theKey].append([(row+1), (column+1)])
                                else: positions.append([row+1, column+1])
                            
                            if(checker(row, 1) and checker(column, -1)):
                                if theKey in targeted: targeted[theKey].append([row+1, column-1])
                                else: positions.append([row+1, column-1])

                    case 'rook':
                        if theKey in targeted:
                            theMoves = rookMoves(nodePosition, grid)
                            for x in theMoves:
                                targeted[theKey].append(x)
                        else:  
                            positions = rookMoves(nodePosition, grid)
                    
                    case 'knight':
                        if theKey in targeted:
                            theMoves = knightMoves(nodePosition, grid)
                            for x in theMoves:
                                targeted[theKey].append(x)
                        else:
                            positions = knightMoves(nodePosition, grid)
                    
                    case 'bishop': 
                        if theKey in targeted:
                            theMoves = bishopMoves(nodePosition, grid)
                            for x in theMoves:
                                targeted[theKey].append(x)
                        else: 
                            positions = bishopMoves(nodePosition, grid)
                    case 'king': positions = kingMoves(nodePosition, grid)
                    case 'queen': positions = queenMoves(nodePosition, grid)
                
                if theKey not in targeted:
                    targeted[theKey] = positions
            else: 
                pass
    return targeted

def checkForPins(grid,piecePosition,kingmoves):
    '''
    checkForPins(grid, kingmoves) is a function that is going to take in the grid holding the current
    board matrix, as well as the list of king moves. It is going to go through king moves and compare it 
    to all pieces current moves they can use by using our function updateTargeted() to grab all possible
    pieces and the positions they can take pieces from. With this info we are going to prevent our king 
    from moving to a position that would pin them
    '''
    pieceRow, pieceColumn = piecePosition
    pinnedLocations = updateTargeted(grid)
    newKingMoves = []
    cantMoveTo = []
    for x in kingmoves:
        for key in pinnedLocations:
            team, role = key.split("_")

            # Checks to see if we are looking at a team piece move set, if so we ignore it
            if(team == grid[pieceRow][pieceColumn].piece.team):
                pass
            else:
                # Goes through the list of moves from the enemy piece, and see if one of our king moves
                # lands on a position a enemy can take a piece from 
                for value in pinnedLocations[key]:
                    if(x == value):
                        cantMoveTo.append(x)
    # Checks to see if there are any positions we can't move to, and if so removes it from our 
    # new moves list with the updated information to prevent us from pinning ourselves
    for x in kingmoves:
        if(x not in cantMoveTo):
            newKingMoves.append(x)

    return cantMoveTo, newKingMoves

class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(row * width)
        self.y = int(col * width)
        self.colour = WHITE
        self.piece = None

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.colour, (self.x, self.y, WIDTH / ROWS, WIDTH / ROWS))
        if self.piece:
            WIN.blit(self.piece.image, (self.x, self.y))


def update_display(win, grid, rows, width):
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

def make_grid(rows, width, test):
    '''
    make_grid(int rows, int width) initializes the chess board, and places all pieces 
    where they belong at the start of the game. Each piece on the board is represented
    by a class Node() attribute .piece, which holds a class instance of 
    Piece(string team, string role), storing info on the Piece's attributes
    
    Parameters:
    - rows: Integer type, represents how many rows our board should have
    - width: Integer type, represents how big pixel wise our board is going to be
    '''
    grid = []
    #width is 800, rows is 8
    gap = width// rows # Gap = 800 / 8 = 100px between each piece
    count = 0

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(j,i, gap)
            if abs(i-j) % 2 == 0:
                node.colour=BLACK
            # test will dictacte if the board is set up according to given test case
            match i:
                case 0:
                    if not test:
                        match j:
                            case 0 | 7: node.piece = Piece('Black', 'rook')
                            case 1 | 6: node.piece = Piece('Black', 'knight')
                            case 2 | 5: node.piece = Piece('Black', 'bishop')
                            case 3: node.piece = Piece('Black', 'queen')
                            case _: node.piece = Piece('Black', 'king') 
                    else:
                        match j:
                            case 1: node.piece = Piece('White', 'king')
                            case 2: node.piece = Piece('White', 'rook')
                            case 4: node.piece = Piece('White', 'queen')
                            case 5: node.piece = Piece('White', 'bishop')
                            case 7: node.piece = Piece('White', 'rook')
                case 1: 
                    if not test:
                        node.piece = Piece('Black', 'pawn')
                    else:
                        match j:
                            case 0 | 1 | 2 | 4 | 5 | 6 | 7:
                                node.piece = Piece('White', 'pawn')
                case 2:
                    if test:
                        match j:
                            case 2: node.piece = Piece('White', 'knight')

                case 3:
                    if test:
                        match j:
                            case 3: node.piece = Piece('White', 'pawn')
                            case 7: node.piece = Piece('White', 'knight')

                case 4:
                    if test:
                        match j:
                            case 3: node.piece = Piece('Black', 'pawn')
                            case 6: node.piece = Piece('White', 'bishop')

                case 5:
                    if test:
                        match j:
                            case 0: node.piece = Piece('Black', 'queen')
                            case 2 | 5: node.piece = Piece('Black', 'knight')
                            case 3: node.piece = Piece('Black', 'bishop')
                            case 4: node.piece = Piece('Black', 'pawn')
                            
                case 6:
                    if not test: 
                        node.piece = Piece('White', 'pawn')
                    else:
                        match j:
                            case 0 | 1 | 2 | 5 | 6 | 7: node.piece = Piece('Black', 'pawn')
                            case 3: node.piece = Piece('Black', 'bishop')
                case 7:
                    if not test:
                        match j:
                            case 0 | 7: node.piece = Piece('White', 'rook')
                            case 1 | 6: node.piece = Piece('White', 'knight')
                            case 2 | 5: node.piece = Piece('White', 'bishop')
                            case 3: node.piece = Piece('White', 'queen')
                            case _: node.piece = Piece('White', 'king')
                    else:
                        match j:
                            case 0: node.piece = Piece('Black', 'rook')
                            case 3: node.piece = Piece('Black', 'king')
                            case 7: node.piece = Piece('Black', 'rook')
            count+=1
            grid[i].append(node)
    return grid


def draw_grid(win, rows, width):
    gap = width // ROWS
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))

def outputGrid(grid):
    viewableMatrix =[]                      
    '''
    outputGrid(list grid) is a function used to display how the board grid threw terminal.
    Helping better understand how we are maneuvering this matrix to move pieces and 
    calculate the logic

    Parameters:
    - grid: A matrix made from lists representing the board
    '''    
    for row in range(len(grid)):
        viewableMatrix.append([])
        for column in range(len(grid)):
            if(grid[row][column].piece):
                viewableMatrix[row].append("X")
            else: 
                viewableMatrix[row].append(" ")
        print(viewableMatrix[row])
    
    #This can be uncommented if needed to be used for reference later in code
    #return viewableMatrix

class Piece:
    '''
    Piece class holds the various object variables for each Piece instance created
    for our chess board.
    
    Attributes of Piece:
    - team: The team of the piece, either Black or White
    - role: The role the piece is, either pawn, rook, knight, bishop, queen, or king
    - pinned: Whether the piece is pinned or not, may not be useful to all pieces
    - checked: Whether the piece is checked or not, may not be useful to all pieces
    - first_move: Whether the piece is using it's first move, may not be useful to all pieces
    - can_castle: Used to check if we are able to castle a rook and king
    - targets: dictionary that stores every piece's next possible position moves, used so that
      the king piece can see positions they are not allowed to move in
    '''
    def __init__(self, team, role):
        self.team=team
        self.role = role
        self.pinned = False
        self.checked = False
        self.first_move = True

        match self.team:
            case 'Black':
                match self.role:
                    case 'pawn': self.image=BPAWN
                    case 'rook': self.image=BROOK
                    case 'knight': self.image=BKNIGHT
                    case 'bishop': self.image=BBISHOP
                    case 'queen': self.image=BQUEEN    
                    case 'king': self.image=BKING
            case 'White':
                match self.role:
                    case 'pawn': self.image=WPAWN
                    case 'rook': self.image=WROOK
                    case 'knight': self.image=WKNIGHT
                    case 'bishop': self.image=WBISHOP
                    case 'queen': self.image=WQUEEN    
                    case 'king': self.image=WKING
            case _:
                print("WE ARE IN A DEFAULT CASE WE SHOULDN'T BE")
        self.type=None
              
    
    def updatePin(self):
        self.pinned = not self.pinned

    def updateCheck(self):
        self.checked = not self.checked
    
    def updateMoved(self):
        self.first_move = False

    def draw(self, x, y):
        WIN.blit(self.image, (x,y))


def getNode(grid, rows, width):
    gap = width//rows
    ColX,RowY = pygame.mouse.get_pos()
    Row = RowY//gap
    Col = ColX//gap
    return (Row,Col)


def resetColours(grid, node):
    '''
    resetColours(grid, node) is a function that views the previous clickedNode's potentialMoves,
    and removes the blue tiles showing the possible moves, and sets it back to the regular board.

    Parameters:
    - grid: The current grid holding the board
    - node: The current node that the player has selected 
    '''
    positions = generatePotentialMoves(node, grid)
    positions.append(node)

    for colouredNodes in positions:
        nodeX, nodeY = colouredNodes
        grid[nodeX][nodeY].colour = BLACK if abs(nodeX - nodeY) % 2 == 0 else WHITE

def HighlightpotentialMoves(piecePosition, grid):
    positions = generatePotentialMoves(piecePosition, grid)
    # Highlighting positions red that the king can not go to, if the piece is a king
    pieceRow, pieceColumn = piecePosition


    if(grid[pieceRow][pieceColumn].piece.role == 'king'):
        pinnedInfo = checkForPins(grid,piecePosition,positions)
        cantMoveTo, positions = pinnedInfo

    for position in positions:
        Row,Column = position
        grid[Row][Column].colour=BLUE
    
    if(grid[pieceRow][pieceColumn].piece.role == 'king'):
        for position in cantMoveTo:
            Row, Column = position
            grid[Row][Column].colour=RED

def opposite(team):
    return "Black" if team=="White" else "White"

def generatePotentialMoves(nodePosition, grid):
    '''
    generatePotentialMoves(nodePosition, grid) is used to call the appropriate module to calculate the 
    available moves based on the piece chosen. 
    '''
    # checker = lambda x,y: x+y>=0 and x+y<8
    positions= []
    row, column = nodePosition
    if(grid[row][column].piece):
        match grid[row][column].piece.role:
            case 'pawn': positions = pawnMoves(nodePosition, grid)
            case 'rook': positions = rookMoves(nodePosition, grid)
            case 'knight': positions = knightMoves(nodePosition, grid)
            case 'bishop': positions = bishopMoves(nodePosition, grid)
            case 'king': positions = kingMoves(nodePosition, grid)
            case 'queen': positions = queenMoves(nodePosition, grid)
    else:
        print("Trying to grab positions from a node that doesnt exist!")

    return positions


def highlight(ClickedNode, grid, OldHighlight):
    Row, Column = ClickedNode
    grid[Row][Column].colour=ORANGE
    if(OldHighlight):
        resetColours(grid, OldHighlight)
    HighlightpotentialMoves(ClickedNode, grid)
    return (Row,Column)

def move(grid, piecePosition, newPosition):
    resetColours(grid, piecePosition)

    # Declarations used, newPosition holds the position on the board we are moving our current piece to, piecePosition holds
    # the current piece we are trying to move, piece is the class attribute of piecePosition, and newPiece is the class 
    # attribute of newPosition
    newRow, newColumn = newPosition
    oldRow, oldColumn = piecePosition
    piece = grid[oldRow][oldColumn].piece
    newPiece = grid[newRow][newColumn].piece

    if(newPiece):
        # Checks if the selected piece is a rook
        if(newPiece.role == 'rook' and piece.role == 'king'):
            # Checks if the moving piece is a king, meaning that the player is choosing to castle
            if grid[oldRow][oldColumn].piece.role == 'king':
                if grid[oldRow][oldColumn].piece.team == grid[newRow][newColumn].piece.team:
                    # Saves piece information from old nodes and then deletes the pieces from those nodes
                    rook = grid[newRow][newColumn].piece
                    king = grid[oldRow][oldColumn].piece
                    grid[newRow][newColumn].piece = None
                    grid[oldRow][oldColumn].piece = None           
                    # Checks direction of castle
                    if oldColumn - newColumn < 0:
                        # We are moving right
                        if king.team == 'Black' and newRow == 7:
                            # Handles if Black is on bottom
                            grid[newRow][newColumn-2].piece = king
                            grid[newRow][newColumn-3].piece = rook
                            # Updates newColumn to the actual square the king will be moved to
                            newColumn = newColumn-2
                        else:
                            # Handles if White is on bottom
                            grid[newRow][newColumn-1].piece = king
                            grid[newRow][newColumn-2].piece = rook
                            # Updates newColumn to the actual square the king will be moved to
                            newColumn = newColumn-1
                    else:
                        # We are moving left
                        if king.team == 'Black' and newRow == 7:
                            # Handles if black is on bottom
                            grid[newRow][newColumn+1].piece = king
                            grid[newRow][newColumn+2].piece = rook
                            # Update newColumn to the actual square that the king will be moved to
                            newColumn = newColumn+1
                        else:
                            # Handles if White is on bottom
                            grid[newRow][newColumn+2].piece = king
                            grid[newRow][newColumn+3].piece = rook
                            # Update newColumn to the actual square that the king will be moved to
                            newColumn = newColumn+2
                else:
                    grid[oldRow][oldColumn].piece = None
                    grid[newRow][newColumn].piece = piece
            # Takes piece if the selected piece is not a king
            else:
                grid[oldRow][oldColumn].piece = None
                grid[newRow][newColumn].piece = piece
        else:
            # Moving piece takes over node, a piece has been taken
            grid[oldRow][oldColumn].piece = None
            grid[newRow][newColumn].piece = piece
    else:
        # No piece on this node, moving piece moves here
        grid[newRow][newColumn].piece = piece
        grid[oldRow][oldColumn].piece = None

    # Check to see if this was the piece's first move, if so then change first move value to false
    if(grid[newRow][newColumn].piece.first_move):
        grid[newRow][newColumn].piece.first_move = False

    # Next player's turn
    return opposite(grid[newRow][newColumn].piece.team)




def chess(WIDTH, ROWS, test):
    grid = make_grid(ROWS, WIDTH, test)
    #outputGrid(grid)
    highlightedPiece = None
    currMove = 'White'
    #consider adding way to exit back to main.py
    while True:
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                print('EXIT SUCCESSFUL')
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print('EXIT SUCCESSFUL')
                    pygame.quit()
                    sys.exit()


            if event.type == pygame.MOUSEBUTTONDOWN:
                #print("Mouse Button was clicked")
                clickedNode = getNode(grid, ROWS, WIDTH)
                #print("ClickedNode was created using getNode(grid,ROWS, WIDTH)")
                ClickedPositionRow, ClickedPositionColumn = clickedNode
                #print(f"Clicked Nodes Row: {ClickedPositionRow}, Clicked Nodes Column: {ClickedPositionColumn}")
                
                # Checks to see if we clicked an available move
                if grid[ClickedPositionRow][ClickedPositionColumn].colour == BLUE:
                    if highlightedPiece:
                        pieceRow, pieceColumn = highlightedPiece
                    # Checks to see if it is this pieces turn to go, which if the colour is BLUE it is either way,
                    # however it makes it so it changes the currMove to now be set to the team as the next move
                    if currMove == grid[pieceRow][pieceColumn].piece.team:
                        #resetColours(grid, highlightedPiece)
                        currMove=move(grid, highlightedPiece, clickedNode)
                        highlightedPiece = None
                # Checks to see if we clicked the same piece over again, so nothing changed
                elif highlightedPiece == clickedNode:
                    pass
                else:
                    # Checks if the spot we clicked holds a piece
                    if grid[ClickedPositionRow][ClickedPositionColumn].piece:
                        # Then checks if its this pieces turn to go, compares to currMove, which holds what piece's 
                        # turn it is
                        if currMove == grid[ClickedPositionRow][ClickedPositionColumn].piece.team:
                            # We declare here what highlightedPiece is, instead of it being none. Basically
                            # stores what piece did we click on
                            highlightedPiece = highlight(clickedNode, grid, highlightedPiece)


        update_display(WIN, grid,ROWS,WIDTH)
