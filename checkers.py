########################################################
# CMPS 3500 - Class Project
# Checkers game simulator
# This is a program that will simulate a checkers board
# and provide basic game functionalities.
# This program does not abide all the rules of checkers
########################################################

import pygame
import pygame.freetype
import random
import sys
from itertools import combinations
import os

# current directory
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'relative/path/to/file/you/want')


WIDTH = 800
ROWS = 8

RED= pygame.image.load(os.path.join(dirname, 'images/red.png'))
GREEN= pygame.image.load(os.path.join(dirname, 'images/green.png'))

REDKING = pygame.image.load(os.path.join(dirname, 'images/redking.png'))
GREENKING = pygame.image.load(os.path.join(dirname, 'images/greenking.png'))

WHITE = (255,255,255)
BLACK = (0,0,0)
ORANGE = (235, 168, 52)
BLUE = (76, 252, 241)


pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Arial', 48)
red_win_prompt = my_font.render('RED WINS', False, (255,0,0))
green_win_prompt = my_font.render('GREEN WINS', False, (255,0,0))
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption('Checkers')

swap = False
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


def make_grid(rows, width, test):
    '''
    make_grid(int rows, int width) initializes the checkers board, and places all pieces 
    where they belong at the start of the game. Each piece on the board is represented
    by a class Node() attribute .piece, which holds a class instance of 
    Piece(string team, string role), storing info on the Piece's attributes
    
    Parameters:
    - rows: Integer type, represents how many rows our board should have
    - width: Integer type, represents how big pixel wise our board is going to be
    '''
    grid = []
    gap = width// rows
    count = 0
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(j,i, gap)
            if abs(i-j) % 2 == 0:
            #print(f"if abs(i-j) % 2 == 0 so we set node.colour to Black")
                node.colour=BLACK
            if not test:
                if (abs(i+j)%2==0) and (i<3):
                    #print(f"node.piece = Red")
                    node.piece = Piece('R')
                elif(abs(i+j)%2==0) and i>4:
                    #print(f"node.piece = Green")
                    node.piece=Piece('G')
            else:
                match i:
                    case 0:
                        match j:
                            case 0 | 4: node.piece = Piece('R')
                    case 1:
                        match j:
                            case 3 | 5 | 7: node.piece = Piece('R')   
                    case 2:
                        match j:
                            case 0 | 6: node.piece = Piece('R')
                    case 3:
                        match j:
                            case 1: node.piece = Piece('R')
                            case 3: node.piece = Piece('G')
                    case 5:
                        match j:
                            case 1 | 3 | 7: node.piece = Piece('G')
                    case 6:
                        match j:
                            case 0 | 2 | 6: node.piece = Piece('G')
                    case 7:
                        match j:
                            case 3: 
                                node.piece = Piece('R')
                                node.piece.type = 'KING'
                                node.piece.image = REDKING

            count+=1
            grid[i].append(node)
    return grid


def draw_grid(win, rows, width):
    gap = width // ROWS
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))


class Piece:
    def __init__(self, team):
        self.team=team
        self.image= RED if self.team=='R' else GREEN
        self.type=None

    def draw(self, x, y):
        WIN.blit(self.image, (x,y))


def getNode(grid, rows, width):
    gap = width//rows
    RowX,RowY = pygame.mouse.get_pos()
    Row = RowX//gap
    Col = RowY//gap
    return (Col,Row)


def resetColours(grid, node):
    positions = generatePotentialMoves(node, grid)
    positions.append(node)

    for colouredNodes in positions:
        nodeX, nodeY = colouredNodes
        grid[nodeX][nodeY].colour = BLACK if abs(nodeX - nodeY) % 2 == 0 else WHITE

def HighlightpotentialMoves(piecePosition, grid):
    global swap
    positions = generatePotentialMoves(piecePosition, grid)
    # If there are no potential moves, turn swap to True to trigger a change in player turn
    if not positions:
        swap = True
    for position in positions:
        Column,Row = position
        grid[Column][Row].colour=BLUE


def opposite(team):
    return "R" if team=="G" else "G"

def generatePotentialMoves(nodePosition, grid):
    '''
    generatePotentialMoves(int(x, y), list gridMatrix) is a function that is used to 
    generate the potential moves each piece can make, and grab the coordinates of the 
    possible positions and puts them in a list to be returned
    
    Parameters:
    - nodePosition: The position of the piece that was clicked. Typically placed based on a
      X and Y position within grid
    - grid: A matrix made from lists representing the board
    '''
    #Going to uncomment this out to use to reference PotentialMoves later in code
    #outputGrid(grid)
    checker = lambda x,y: x+y>=0 and x+y<8
    positions= []
    column, row = nodePosition
    # If a piece variable class exists in this list slot within the matrix
    if grid[column][row].piece:
        vectors = [[1, -1], [1, 1]] if grid[column][row].piece.team == "R" else [[-1, -1], [-1, 1]]
        if grid[column][row].piece.type=='KING':
            vectors = [[1, -1], [1, 1],[-1, -1], [-1, 1]]
        for vector in vectors:
            columnVector, rowVector = vector
            # Check to see if all moves the piece can make are possible on the board (if its out of baounds)
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
Error with locating possible moves row col error
"""
def highlight(ClickedNode, Grid, OldHighlight):
    Column,Row = ClickedNode
    Grid[Column][Row].colour=ORANGE
    if OldHighlight:
        resetColours(Grid, OldHighlight)
    HighlightpotentialMoves(ClickedNode, Grid)
    return (Column,Row)

def move(grid, piecePosition, newPosition):
    resetColours(grid, piecePosition)
    newColumn, newRow = newPosition
    oldColumn, oldRow = piecePosition

    piece = grid[oldColumn][oldRow].piece
    grid[newColumn][newRow].piece=piece
    grid[oldColumn][oldRow].piece = None

    if newColumn==7 and grid[newColumn][newRow].piece.team=='R':
        grid[newColumn][newRow].piece.type='KING'
        grid[newColumn][newRow].piece.image=REDKING
    if newColumn==0 and grid[newColumn][newRow].piece.team=='G':
        grid[newColumn][newRow].piece.type='KING'
        grid[newColumn][newRow].piece.image=GREENKING
    if abs(newColumn-oldColumn)==2 or abs(newRow-oldRow)==2:
        grid[int((newColumn+oldColumn)/2)][int((newRow+oldRow)/2)].piece = None
        # This line dictates a second move if piece is captured
        # Need to find a solution to only move again if a second capture is available
        return grid[newColumn][newRow].piece.team
    return opposite(grid[newColumn][newRow].piece.team)

def checkWin(grid):
    # Set up some booleans to check for remaining pieces
    greenWin = False
    redWin = False
    # Iterate through entire board
    for row in range(len(grid)):
        for column in range(len(grid)):
            if grid[row][column].piece:
                if grid[row][column].piece.team == 'G':
                    # if green piece is found, flip to true
                    greenWin = True
                else:
                    # if red piece is found, flip to true
                    redWin = True
    # If all of one color's pieces are gone, return who the winner is
    if redWin and not greenWin:
        return 'RED'
    elif greenWin and not redWin:
        return 'GREEN'
    return None


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
    

def checkers(WIDTH, ROWS, test):
    grid = make_grid(ROWS, WIDTH, test)
    #Uncomment to view how grid is being viewed through terminal
    #outputGrid(grid)
    highlightedPiece = None
    # Some variables to handle multiple moves per turn
    newPosition = None
    currMove = 'G'
    prevMove = 'R'
    clicked = False

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
                        checkers(WIDTH, 8, False)
                    else:
                        checkers(WIDTH, 8, True)
            # Detect and find if piece was pressed, or detect if allowed move was pressed
            # This holds the logic of when pieces are being chosen by a player
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Checks if players turn was same player as last turn
                # This effectively means that the color is moving multiple times per turn
                if currMove == prevMove and not clicked:
                    # Uses position of piece from last turn
                    clickedNode = newPosition
                    # Boolean update to ensure updated note gets chosen on next click
                    clicked = True
                else:
                    # If different players turn, use clicked position
                    clickedNode = getNode(grid, ROWS, WIDTH)
                    clicked = False
                ClickedPositionColumn, ClickedPositionRow = clickedNode
                # if-elif-else statement detecting if your press was a valid move, 
                if grid[ClickedPositionColumn][ClickedPositionRow].colour == BLUE:
                    if highlightedPiece:
                        pieceColumn, pieceRow = highlightedPiece
                    if currMove == grid[pieceColumn][pieceRow].piece.team:
                        resetColours(grid, highlightedPiece)
                        # Saves who's turn it is to compare with the next turn
                        prevMove=currMove
                        # Saves the new position of the moved piece
                        newPosition = clickedNode
                        currMove=move(grid, highlightedPiece, clickedNode)
                elif highlightedPiece == clickedNode:
                    pass
                else:
                    if grid[ClickedPositionColumn][ClickedPositionRow].piece:
                        if currMove == grid[ClickedPositionColumn][ClickedPositionRow].piece.team:
                            highlightedPiece = highlight(clickedNode, grid, highlightedPiece)
                            # Swap variable used to handle the scenario in which a piece that is allowed to move twice has no available moves
                            global swap
                            if swap:
                                # If it was decided a swap needs to happen, then the next turn will go to the opposite player
                                currMove = opposite(grid[ClickedPositionColumn][ClickedPositionRow].piece.team)
                                swap = False
        winner = checkWin(grid)
        # If we return a value from checkWin(), we end the game and display the winner
        if winner:
            if winner == 'RED':
                WIN.blit(red_win_prompt, (WIDTH/2.7, WIDTH/2.5))
            else:
                WIN.blit(green_win_prompt, (WIDTH/2.7, WIDTH/2.5))    
        else:
            update_display(WIN, grid,ROWS,WIDTH)
        pygame.display.flip()


#checkers(WIDTH, ROWS)