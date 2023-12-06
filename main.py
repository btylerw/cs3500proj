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
checkers_test_prompt = my_font.render('Press 3 for Checkers Test', False, (255, 255, 255))
chess_test_prompt = my_font.render('Press 4 for Chess Test', False, (255, 255, 255))
main_exit_prompt = my_font.render('Press ESC to exit', False, (255,255,255))
helper_prompt = my_font.render('Press 1 while in game to reset', False, (255,255,255))
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption('Main')
# *_start variables are used to determine if we automatically start a game again (game has been reset)
chess_start = 0
checkers_start = 0
# Keep track of our test condition
test = False

while True:
    for event in pygame.event.get():
        if chess_start:
            # To reset chess board
            chess_start, test = chess(WIDTH, 8, test)
        elif checkers_start:
            # To reset checkers board
            checkers_start, test = checkers(WIDTH, 8, test)
        if event.type== pygame.QUIT:
            print('EXIT SUCCESSFUL')
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                # Start up normal checkers, returning values dictate if we automatically restart next loop
                checkers_start, test = checkers(WIDTH, 8, False)
            if event.key == pygame.K_2:
                # Start up normal chess, returning values dictate if we automatically restart next loop
                chess_start, test = chess(WIDTH, 8, False)
            if event.key == pygame.K_3:
                # Start up test checkers, returning values dictate if we automatically restart next loop
                checkers_start, test = checkers(WIDTH, 8, True)
            if event.key == pygame.K_4:
                # Start up test chess, returning values dictate if we automatically restart next loop
                chess_start, test = chess(WIDTH, 8, True)
            if event.key == pygame.K_ESCAPE:
                print('EXIT SUCCESSFUL')
                pygame.quit()
                sys.exit()
    if not chess_start and not checkers_start:
        WIN.blit(checkers_prompt, (WIDTH/4,WIDTH/3))
        WIN.blit(chess_prompt, (WIDTH/4,WIDTH/2.4))
        WIN.blit(checkers_test_prompt, (WIDTH/4,WIDTH/2))
        WIN.blit(chess_test_prompt, (WIDTH/4,WIDTH/1.7))
        WIN.blit(main_exit_prompt, (WIDTH/4,WIDTH/1.5))
        WIN.blit(helper_prompt, (WIDTH/5.8, WIDTH/1.3))
        pygame.display.flip()