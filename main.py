################################
# BEGINNING OF MAIN PROJECT FILE
# Student 1: Tyler Brown
# Student 2: Douglas Cerrato
# Student 3: Stephen Marks
# Student 4: Raul Velasco
################################

import pygame
import pygame.freetype
import sys
import os

# Function names in checkers.py will likely need to be changed for compatability
# main function name will absolutely need to be changed, and the call to it will need to be done in here
from checkers import *
from chess import *

WIDTH = 800

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Arial', 48)
checkers_prompt = my_font.render('Press 1 for Checkers', False, (255, 255, 255))
chess_prompt = my_font.render('Press 2 for Chess', False, (255, 255, 255))
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption('Main')

while True:
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            print('EXIT SUCCESSFUL')
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                checkers(WIDTH, 8)
            if event.key == pygame.K_2:
                chess(WIDTH, 8)
    WIN.blit(checkers_prompt, (WIDTH/4,WIDTH/3))
    WIN.blit(chess_prompt, (WIDTH/4,WIDTH/2.4))
    pygame.display.flip()