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

pygame.font.init()
my_font = pygame.font.SysFont('Arial', 48)
black_win_prompt = my_font.render('Black Wins!', False, (0, 0, 0))
white_win_prompt = my_font.render('White Wins!', False, (0, 0, 0))
draw_prompt = my_font.render('Draw!', False, (0, 0, 0))
restart_prompt = my_font.render('Restart Game: 1', False, (0, 0, 0))
main_menu_prompt = my_font.render('Main Menu: 2', False, (0, 0, 0))
exit_prompt = my_font.render('Exit: ESC', False, (0, 0, 0))

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

def checkForCheckmate(grid, attackers, king_moves, king_position):
    '''
    Function that is used to check all possible moves for each team after every move to determine if there is an end condition
    Iterates through entire board and calls HighlightpotentialMoves for every piece to give us this number.
    '''
    # Creating some counters for each team's possible moves
    black_moves = 0
    white_moves = 0
    for row in range(len(grid)):
        for column in range(len(grid)):
            if grid[row][column].piece:
                pos = [row, column]
                if grid[row][column].piece.team == 'Black':
                    # If the piece is black add all of it's moves to our black_moves counter
                    black_moves += HighlightpotentialMoves(pos, grid, attackers, king_moves, king_position, True)
                elif grid[row][column].piece.team == 'White':
                    # If the piece is white add all of it's moves to our white_moves counter
                    white_moves += HighlightpotentialMoves(pos, grid, attackers, king_moves, king_position, True)
    # Return both move counts
    return black_moves, white_moves

def checkForCheck(grid):
    '''
    A function to determine if a king is in check.
    Gets a dictionary of all attacked nodes and then finds the positions of both kings and checks if the kings are on an attacked node
    If a king is on an attacked node, it changes every single piece of that color's checked property to true. If a king is not in check it
    ensures that the checked value is false.
    '''
    # Returns to us all attacking pieces 
    attackedNodes = updateTargeted(grid)
    # A list that will give us the current positions of each king
    king_moves = []
    king_position = []
    attackers = {}
    # We will update these with the position of a checked king if a check is found
    checked_row = -1
    checked_column = -1
    # We will update this with the color of the checked king
    checked_color = None
    # Iterate through grid to find each king and save their locations
    for row in range(len(grid)):
        for column in range(len(grid)):
            if (grid[row][column].piece):
                if (grid[row][column].piece.role == 'king'):
                    king_moves.append([row, column])

    # Iterate through attackedNodes and find if a piece is currently attacking the king
    # key = A piece in the list in "role, team" format
    for key in attackedNodes:
        team, role = key.split("_")
        # Check each nodes that each piece is attacking
        for node in attackedNodes[key]:
            # If an attacked node is a king node, we update our checked_column, checked_row values to the king node
            if node in king_moves:
                attackers[key] = attackedNodes[key]
                checked_row, checked_column = node
                # Ensuring we don't check the king of the same team
                if (grid[checked_row][checked_column].piece.team) == team:
                    checked_row = -1
                    checked_column = -1
    king_moves = []
    # If no check is found, we ensure all piece's checked values are False
    if checked_row and checked_column < 0:
        for row in range(len(grid)):
            for column in range(len(grid)):
                if (grid[row][column].piece):
                    grid[row][column].piece.checked = False
    # A check has been found
    elif checked_column > -1 and checked_row > -1:
        # Set king's checked value to true
        grid[checked_row][checked_column].piece.checked = True
        nodePosition = checked_row, checked_column
        king_position = nodePosition
        king_moves = kingMoves(nodePosition, grid)
        # Save the color of the king
        checked_color = grid[checked_row][checked_column].piece.team
        for row in range(len(grid)):
            for column in range(len(grid)):
                newnode = grid[row][column]
                if newnode.piece:
                    # Find all pieces with the same color as the king and change their checked value to True
                    if newnode.piece.team == checked_color:
                        newnode.piece.checked = True
    
    return attackers, king_moves, king_position



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
                        if(grid[row][column].piece.bottom):
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

    If piece is not a king, we check if it sits on a node that is being attacked. If it is and the attacking piece is not a knight,
    we scan adjacent nodes to find another attacked node so that we can determine direction of attack and check if the piece is between
    the attacker and king. If it is, that piece is now pinned. If it's not, we ensure the piece is not pinned.
    '''
    pieceRow, pieceColumn = piecePosition
    pinnedLocations = updateTargeted(grid)
    newKingMoves = []
    cantMoveTo = []
    attack_vectors = []

    if grid[pieceRow][pieceColumn].piece.role == 'king':
        for x in kingmoves:
            for key in pinnedLocations:
                team, role = key.split("_")

                # Checks to see if we are looking at a team piece move set, if so we ignore it
                if(team == grid[pieceRow][pieceColumn].piece.team):
                    pass
                elif grid[pieceRow][pieceColumn].piece.checked:
                    for value in pinnedLocations[key]:
                        if x == value:
                            cantMoveTo.append(x)
                            # If the attacker is a knight or a pawn we can ignore
                            if role != 'knight' and role != 'pawn':
                                # Get attack vector
                                vrow, vcolumn = x
                                vrow = pieceRow - vrow
                                vcolumn = pieceColumn - vcolumn
                                # Ensure we are not checking out of bounds
                                if pieceRow+vrow < 8 and pieceColumn+vcolumn < 8 and pieceRow+vrow >= 0 and pieceColumn+vcolumn >= 0:
                                    # Add movement square behind king to list
                                    cantMoveTo.append([pieceRow+vrow, pieceColumn+vcolumn])
                else:
                    # Goes through the list of moves from the enemy piece, and see if one of our king moves
                    # lands on a position a enemy can take a piece from 
                    for value in pinnedLocations[key]:
                        if(x == value):
                            cantMoveTo.append(x)
    else:
        # Checking all attackers
        for key in pinnedLocations:
            team, role = key.split("_")
            # Ignore if the attacker is on the same team
            # Ignore if the attacker is a knight
            if [pieceRow, pieceColumn] in pinnedLocations[key] and role != 'knight' and role != 'pawn' and team != grid[pieceRow][pieceColumn].piece.team:
                    # We check all adjacent nodes for the attacker, or for another node under attack
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            # Ensure we remain in bounds
                            if i != 0 or j != 0:
                                if pieceRow+i < 8 and pieceColumn+j < 8:
                                    # Save the position we're checking
                                    attackpos = [pieceRow+i, pieceColumn+j]
                                    # We've found a piece
                                    if grid[pieceRow+i][pieceColumn+j].piece:
                                        # If the piece is on the same team, ignore it
                                        # If the piece is the same piece as the current attacker, add i, j to our vector list
                                        if grid[pieceRow+i][pieceColumn+j].piece.role == role and len(attack_vectors) == 0 and grid[pieceRow+i][pieceColumn+j].piece.team != grid[pieceRow][pieceColumn].piece.team:
                                            attack_vectors.append(-i)
                                            attack_vectors.append(-j)
                                    # If the current position is in the attacker's attacked node list, add i, j to our vector list
                                    elif attackpos in pinnedLocations[key] and len(attack_vectors) == 0:
                                        attack_vectors.append(-i)
                                        attack_vectors.append(-j)
        # Making sure there are two values in attack_vectors
        if len(attack_vectors) == 2:
            # We're going to be using these variables to check along attack direction
            vrow, vcolumn = attack_vectors
        else:
            # If there aren't two values in attack_vectors, then we have no vector
            vcolumn = 0
            vrow = 0
        # If we have no vector, then the piece is not pinned and can freely move
        if vcolumn == 0 and vrow == 0:
            grid[pieceRow][pieceColumn].piece.pinned = False
        # Check for a pin if we have a vector
        else:
            # Temp variables so we do not overwrite our original position
            trow = pieceRow
            tcolumn = pieceColumn
            # Ensure we do not go out of bounds
            while trow + vrow < 8 and tcolumn + vcolumn < 8:
                # Move to each position along the vector
                trow += vrow
                tcolumn += vcolumn
                # Check if there is a piece on the new node
                if grid[trow][tcolumn].piece:
                    # If the first encountered piece is our king, then this piece is now pinned
                    if grid[trow][tcolumn].piece.team == grid[pieceRow][pieceColumn].piece.team and grid[trow][tcolumn].piece.role == 'king':
                        grid[pieceRow][pieceColumn].piece.pinned = True
                        break
                    # If not, then we are not pinned
                    else:
                        grid[pieceRow][pieceColumn].piece.pinned = False
                        break

    # Checks to see if there are any positions we can't move to, and if so removes it from our 
    # new moves list with the updated information to prevent us from pinning ourselves
    for x in kingmoves:
        if(x not in cantMoveTo):
            newKingMoves.append(x)

    return cantMoveTo, newKingMoves, attack_vectors

#TODO: Create docstrings for this function, and set it up so it does all the gui for the piece swap, as well as 
# handling what piece gets replaced for the pawn
def pawnEndBoard(nodePosition, grid): 
    nodeRow, nodeColumn = nodePosition
    pieceBottomPerspective = grid[nodeRow][nodeColumn].piece.bottom

    if(pieceBottomPerspective):
        if(nodeRow == 0):
            print("We have hit a pawn at the end of the board")
    else:
            print("We have hit a pawn at the end of the board")

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


def update_display(win, grid, rows, width, white_win, black_win, draw):
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    # Checking if the game is over to display pertinent information
    if white_win or black_win or draw:
        # White wins, display appropriate prompt
        if white_win:
            WIN.blit(white_win_prompt, (WIDTH/4, WIDTH/3))
        # Black wins, display appropriate prompt
        elif black_win:
            WIN.blit(black_win_prompt, (WIDTH/4, WIDTH/3))
        # It's a draw, display appropriate prompt
        elif draw:
            WIN.blit(draw_prompt, (WIDTH/4, WIDTH/3))
        # Display available actions for when game is over
        WIN.blit(restart_prompt, (WIDTH/4,WIDTH/2.4))
        WIN.blit(main_menu_prompt, (WIDTH/4,WIDTH/2))
        WIN.blit(exit_prompt, (WIDTH/4,WIDTH/1.7))

            
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
                            case 0 | 7: node.piece = Piece('Black', 'rook', False)
                            case 1 | 6: node.piece = Piece('Black', 'knight', False)
                            case 2 | 5: node.piece = Piece('Black', 'bishop', False)
                            case 3: node.piece = Piece('Black', 'queen', False)
                            case _: node.piece = Piece('Black', 'king', False) 
                    else:
                        match j:                            
                            case 0: node.piece = Piece('Black', 'rook', False)
                            case 4: node.piece = Piece('Black', 'king', False)
                            case 7: node.piece = Piece('Black', 'rook', False)

                case 1: 
                    if not test:
                        node.piece = Piece('Black', 'pawn', False)
                    else:
                        match j:                            
                            case 0 | 1 | 2 | 5 | 6 | 7: node.piece = Piece('Black', 'pawn', False)
                            case 4: node.piece = Piece('Black', 'bishop', False)

                case 2:
                    if test:
                        match j:
                            case 7: node.piece = Piece('Black', 'queen', False)
                            case 2 | 5: node.piece = Piece('Black', 'knight', False)
                            case 4: node.piece = Piece('Black', 'bishop', False)
                            case 3: node.piece = Piece('Black', 'pawn', False)

                case 3:
                    if test:
                        match j:                            
                            case 1: node.piece = Piece('White', 'bishop', True)
                            case 4: node.piece = Piece('Black', 'pawn', False)



                case 4:
                    if test:
                        match j:
                            case 0: node.piece = Piece('White', 'knight', True)
                            case 4: node.piece = Piece('White', 'pawn', True)

                case 5:
                    if test:
                        match j:
                            case 5: node.piece = Piece('White', 'knight', True)

                            
                case 6:
                    if not test: 
                        node.piece = Piece('White', 'pawn', True)
                    else:
                        match j:
                            case 0 | 1 | 2 | 3 | 5 | 6 | 7:
                                node.piece = Piece('White', 'pawn', True)

                case 7:
                    if not test:
                        match j:
                            case 0 | 7: node.piece = Piece('White', 'rook', True)
                            case 1 | 6: node.piece = Piece('White', 'knight', True)
                            case 2 | 5: node.piece = Piece('White', 'bishop', True)
                            case 3: node.piece = Piece('White', 'queen', True)
                            case _: node.piece = Piece('White', 'king', True)
                    else:
                        match j:
                            case 0: node.piece = Piece('White', 'rook', True)
                            case 2: node.piece = Piece('White', 'bishop', True)
                            case 3: node.piece = Piece('White', 'queen', True)
                            case 5: node.piece = Piece('White', 'rook', True)
                            case 6: node.piece = Piece('White', 'king', True)

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
    def __init__(self, team, role, bottom):
        self.team=team
        self.role = role
        self.pinned = False
        self.checked = False
        self.first_move = True
        self.bottom = bottom

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

def HighlightpotentialMoves(piecePosition, grid, attackers, king_moves, king_position, checking):
    positions = generatePotentialMoves(piecePosition, grid)
    move_count = 0
    # Highlighting positions red that the king can not go to, if the piece is a king
    pieceRow, pieceColumn = piecePosition


    if(grid[pieceRow][pieceColumn].piece.role == 'king'):
        cantMoveTo, positions, attack_vectors = checkForPins(grid,piecePosition,positions)

    # This will not allow pieces to be moved if checked unless they can move into a king's cantMoveTo space
    # Needs to be reworked so that we can block on the entire vector attacking the king
    # General idea is here though
    if not attackers and not grid[pieceRow][pieceColumn].piece.role == 'king' and not grid[pieceRow][pieceColumn].piece.checked:
        a, b, attack_vectors = checkForPins(grid, piecePosition, positions)
        vrow = 0
        vcolumn = 0
        if not grid[pieceRow][pieceColumn].piece.pinned:
            for position in positions:
                Row,Column = position
                if not checking:
                    grid[Row][Column].colour=BLUE
                else:
                    move_count += 1
        else:
            trow = pieceRow
            tcolumn = pieceColumn
            if attack_vectors:
                vrow = -attack_vectors[0]
                vcolumn = -attack_vectors[1]
            for position in positions:
                Row, Column = position
                trow += vrow
                tcolumn += tcolumn
                if not checking and trow < 8 and tcolumn < 8 and trow == Row and tcolumn == Column:
                    grid[Row][Column].colour=BLUE
                elif checking and trow < 8 and tcolumn < 8 and trow == Row and tcolumn == Column:
                    move_count += 1


    if attackers and not grid[pieceRow][pieceColumn].piece.role == 'king' and grid[pieceRow][pieceColumn].piece.checked:
        canMoveTo = []
        vrow = 0
        vcolumn = 0
        cantMoveTo, b, attack_vectors = checkForPins(grid, king_position, king_moves)
        king_row, king_column = king_position
        for key in attackers:
            team, role = key.split("_")
            for position in positions:
                Row, Column = position
                if grid[Row][Column].piece:
                    if grid[Row][Column].piece.team == team and grid[Row][Column].piece.role == role and not grid[pieceRow][pieceColumn].piece.pinned:
                        if not checking:
                            grid[Row][Column].colour=BLUE
                        else:
                            move_count += 1
            for value in attackers[key]:
                if value in cantMoveTo:
                    #canMoveTo.append(value)
                    # We are using the square the king cannot move to to create a vector in which we can check all potential nodes to block
                    attacker_row, attacker_column = value
                    vrow = attacker_row-king_row
                    vcolumn = attacker_column-king_column

        for key in attackers:
            team, role = key.split("_")
            # Cannot block a check from a knight
            if role != 'knight':
                # temp_pos will be used to check which nodes are available to block on
                temp_row = king_row
                temp_column = king_column
                moves = []
                temp_pos = [temp_row + vrow, temp_column + vcolumn]
                # Continuously checks if our updated position is also an attacked node
                if vrow != 0 or vcolumn != 0:
                    while temp_pos in attackers[key]:
                        tmp = temp_pos
                        # Add node to list
                        moves.append(tmp[:])
                        # Update temp_pos according to attacking vector to check next node
                        temp_pos[0] = temp_pos[0] + vrow
                        temp_pos[1] = temp_pos[1] + vcolumn
                else:
                    if temp_pos in attackers[key]:
                        moves.append(temp_pos[:])
                if temp_pos[0] < 8 and temp_pos[1] < 8:
                    if grid[temp_pos[0]][temp_pos[1]].piece:
                        if grid[temp_pos[0]][temp_pos[1]].piece.team == team and grid[temp_pos[0]][temp_pos[1]].piece.role == role:
                            for move in moves:
                                canMoveTo.append(move)

        for position in positions:
            Row,Column = position
            if position in canMoveTo and not grid[pieceRow][pieceColumn].piece.pinned:
                if not checking:
                    grid[Row][Column].colour=BLUE
                else:
                    move_count += 1

    else:
        for position in positions:
            Row,Column = position
            if not grid[pieceRow][pieceColumn].piece.pinned:
                if not checking:
                    grid[Row][Column].colour=BLUE
                else:
                    move_count += 1
            else:
                trow = pieceRow
                tcolumn = pieceColumn
                if len(attack_vectors) == 2:
                    vrow = attack_vectors[0]
                    vcolumn = attack_vectors[1]
                for position in positions:
                    Row, Column = position
                    trow += vrow
                    tcolumn += tcolumn
                    if not checking and trow < 8 and tcolumn < 8 and trow == Row and tcolumn == Column:
                        grid[Row][Column].colour=BLUE
                    elif checking and trow < 8 and tcolumn < 8 and trow == Row and tcolumn == Column:
                        move_count += 1
    
    if(grid[pieceRow][pieceColumn].piece.role == 'king'):
        for position in cantMoveTo:
            Row, Column = position
            if not checking:
                grid[Row][Column].colour=RED
    
    return move_count

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


def highlight(ClickedNode, grid, OldHighlight, attackers, king_moves, king_position):
    Row, Column = ClickedNode
    grid[Row][Column].colour=ORANGE
    if(OldHighlight):
        resetColours(grid, OldHighlight)
    count = HighlightpotentialMoves(ClickedNode, grid, attackers, king_moves, king_position, False)
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
        elif(piece.role == 'pawn'):
            # Checking to see if piece we picked is a pawn
            #TODO: Set this function call up to work when the piece is MOVING to the end board, not when their starting move position 
            # is the end board
            pawnEndBoard(piecePosition, grid)
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
    attackers = {}
    king_moves = []
    king_position = []
    black_win = False
    white_win = False
    draw = False
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
                if event.key == pygame.K_1:
                    # Resets board
                    if not test:
                        # Return 1 to reset board. False to ensure we don't enter test case
                        return 1, False
                    else:
                        # Return 1 to reset board. True to ensure we enter back into test case
                        return 1, True
                if event.key == pygame.K_2:
                    pygame.display.set_mode((WIDTH, WIDTH))
                    # Return 0 to ensure we go back to main menu
                    return 0, False


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
                            highlightedPiece = highlight(clickedNode, grid, highlightedPiece, attackers, king_moves, king_position)
                attackers, king_moves, king_position = checkForCheck(grid)
                # After every move is made we check for an ending condition
                black_moves, white_moves = checkForCheckmate(grid, attackers, king_moves, king_position)
                # If a team has no moves, then we are in an ending condition
                if black_moves == 0 or white_moves == 0:
                    # Checks if white does not have any moves
                    if not white_moves:
                        for i in range(len(grid)):
                            for j in range(len(grid)):
                                # Goes through board until it finds a piece
                                if grid[i][j].piece:
                                    # If it's a white piece, let's ensure that team is in check
                                    if grid[i][j].piece.team == 'White':
                                        # If it's in check, black has won the game
                                        if grid[i][j].piece.checked:
                                            black_win = True
                                        # If it's not in check, it's a draw
                                        else:
                                            draw = True
                    # Checks if black does not have any moves
                    elif not black_moves:
                        for i in range(len(grid)):
                            for j in range(len(grid)):
                                # Goes through board until it finds a piece
                                if grid[i][j].piece:
                                    # If it's a black piece, let's ensure that team is in check
                                    if grid[i][j].piece.team == 'Black':
                                        # If it's in check, white has won the agme
                                        if grid[i][j].piece.checked:
                                            white_win = True
                                        # If it's not in check, it's a draw
                                        else:
                                            draw = True
        # Updated update_display to check win condition values
        update_display(WIN, grid,ROWS,WIDTH, white_win, black_win, draw)