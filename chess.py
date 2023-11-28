########################################################
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


pygame.init()
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption('Chess')

priorMoves=[]
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

def make_grid(rows, width):
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
            match i:
                case 0:
                    match j:
                        case 0 | 7: node.piece = Piece('Black', 'rook')
                        case 1 | 6: node.piece = Piece('Black', 'knight')
                        case 2 | 5: node.piece = Piece('Black', 'bishop')
                        case 3: node.piece = Piece('Black', 'queen')
                        case _: node.piece = Piece('Black', 'king') 
                case 1: node.piece = Piece('Black', 'pawn')
                case 6: node.piece = Piece('White', 'pawn')
                case 7:
                    match j:
                        case 0 | 7: node.piece = Piece('White', 'rook')
                        case 1 | 6: node.piece = Piece('White', 'knight')
                        case 2 | 5: node.piece = Piece('White', 'bishop')
                        case 3: node.piece = Piece('White', 'queen')
                        case _: node.piece = Piece('White', 'king')
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
    - self.first_move: Whether the piece is using it's first move, may not be useful to all pieces
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

    # ALL Getter Functions
    def getRole(self): return self.role
    def getPinned(self): return self.pinned
    def getChecked(self): return self.checked
    def getFirstMove(self): return self.first_move


    
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
    for position in positions:
        Row,Column = position
        grid[Row][Column].colour=BLUE

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
    # clickedNode, the (row, column) format where the intended piece is supposed to move
    newRow, newColumn = newPosition
    # highlightedPiece, the (row, column) format that should hold the current spot of the piece wanting to be moved 
    oldRow, oldColumn = piecePosition

    # Move the piece on board and remove it from its previous position on the board
    piece = grid[oldRow][oldColumn].piece
    if(grid[newRow][newColumn].piece):
        grid[newRow][newColumn].piece = None
        grid[newRow][newColumn].piece = piece
    else:
        grid[newRow][newColumn].piece = piece
    grid[oldRow][oldColumn].piece = None

    # Check to see if this was the piece's first move, if so then change first move value to false
    if(grid[newRow][newColumn].piece.first_move):
        grid[newRow][newColumn].piece.first_move = False
    
    #outputGrid(grid)

    return opposite(grid[newRow][newColumn].piece.team)




def chess(WIDTH, ROWS):
    grid = make_grid(ROWS, WIDTH)
    #outputGrid(grid)
    highlightedPiece = None
    currMove = 'White'

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