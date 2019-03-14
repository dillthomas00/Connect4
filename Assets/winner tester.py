import pygame
import sys
import random
import numpy
import copy

# General Pygame  Setup
pygame.init()
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen_width, screen_height = screen_width-5, screen_height-75
fpsControl = pygame.time.Clock()

column_count = 11
row_count = 10
board = numpy.zeros((row_count, column_count))

# Image Asset
player_counter = pygame.image.load(".//player_1_winner.png")
(810, 550, 1090, 620)
(810, 650, 1090, 720)
class app():
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.starting_x  = 420
        self.starting_y = 125
        self.displace_x = 98
        self.displace_y = 77.5
        self.player_turn = True
        self.main()

    def main(self):
        grid = pygame.image.load(".//gridtester.png")
        grid = pygame.transform.scale(grid, (1280, 900))
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((255,255,255))
        self.background.blit(grid, (310, 0)) #(1920 - 1280) / 2
        self.screen.blit(self.background, (0,0))

        # Column Buttons  modular to 98
        x1, y1, x2, y2 = 410, 130, 1521, 900
        self.column_area = pygame.Rect(x1, y1, (x2-x1), (y2-y1))
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button.
                        if self.column_area.collidepoint(event.pos):
                            print (event.pos)
                            self.screen.blit(player_counter, (632, 213))
                                
            pygame.display.flip()
            fpsControl.tick(60)
        pygame.quit()
        sys.exit()


app()
