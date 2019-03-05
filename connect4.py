import pygame
import sys
import random
import time

# General Pygame  Setup
pygame.init()
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen_width, screen_height = screen_width-5, screen_height-75
fpsControl = pygame.time.Clock()



column1 = [0,0,0,0,0,0,0,0,0,0] #Bottom to top
column2 = [0,0,0,0,0,0,0,0,0,0] #Bottom to top
column3 = [0,0,0,0,0,0,0,0,0,0] #Bottom to top
column4 = [0,0,0,0,0,0,0,0,0,0] #Bottom to top
column5 = [0,0,0,0,0,0,0,0,0,0] #Bottom to top
column6 = [0,0,0,0,0,0,0,0,0,0] #Bottom to top
column7 = [0,0,0,0,0,0,0,0,0,0] #Bottom to top
column8 = [0,0,0,0,0,0,0,0,0,0] #Bottom to top
column9 = [0,0,0,0,0,0,0,0,0,0] #Bottom to top
column10 = [0,0,0,0,0,0,0,0,0,0] #Bottom to top
column11 = [0,0,0,0,0,0,0,0,0,0] #Bottom to top
column12 = [0,0,0,0,0,0,0,0,0,0] #Bottom to top
column13 = [0,0,0,0,0,0,0,0,0,0] #Bottom to top
column14 = [0,0,0,0,0,0,0,0,0,0] #Bottom to top
column15 = [0,0,0,0,0,0,0,0,0,0] #Bottom to top
column16 = [0,0,0,0,0,0,0,0,0,0] #Bottom to top



# Image Asset
player_counter = pygame.image.load(".//Assets//player_counter.png")
player_counter = pygame.transform.scale(player_counter, (125, 105))

computer_counter = pygame.image.load(".//Assets//computer_counter.png")
computer_counter = pygame.transform.scale(computer_counter, (125, 105))



class app():
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.displace_x = 95
        self.displace_y = 85
        
        self.main()

    def main(self):
        grid = pygame.image.load(".//Assets//grid.png")
        grid = pygame.transform.scale(grid, (1280, 720))
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((255,255,255))
        self.background.blit(grid, (0, 0))
        
        self.screen.blit(self.background, (200, 200))

        # Column Buttons 
        x1, y1, x2, y2 = 0, 0, 120, 950
        self.column1_area = pygame.Rect(x1, y1, (x2-x1), (y2-y1))

        x1, y1, x2, y2 = 120, 0, 240, 950
        self.column2_area = pygame.Rect(x1, y1, (x2-x1), (y2-y1))

        x1, y1, x2, y2 = 240, 0, 360, 950
        self.column3_area = pygame.Rect(x1, y1, (x2-x1), (y2-y1))

        x1, y1, x2, y2 = 360, 0, 480, 950
        self.column4_area = pygame.Rect(x1, y1, (x2-x1), (y2-y1))

        x1, y1, x2, y2 = 480, 0, 600, 950
        self.column5_area = pygame.Rect(x1, y1, (x2-x1), (y2-y1))

        x1, y1, x2, y2 = 600, 0, 720, 950
        self.column6_area = pygame.Rect(x1, y1, (x2-x1), (y2-y1))

        x1, y1, x2, y2 = 720, 0, 840, 950
        self.column7_area = pygame.Rect(x1, y1, (x2-x1), (y2-y1))

        x1, y1, x2, y2 = 840, 0, 960, 950
        self.column8_area = pygame.Rect(x1, y1, (x2-x1), (y2-y1))

        x1, y1, x2, y2 = 960, 0, 1080, 950
        self.column9_area = pygame.Rect(x1, y1, (x2-x1), (y2-y1))

        x1, y1, x2, y2 = 1080, 0, 1100, 950
        self.column10_area = pygame.Rect(x1, y1, (x2-x1), (y2-y1))

        self.screen.blit(player_counter, (120,95))
        self.screen.blit(computer_counter, (500,100))

        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button.
                        print (event.pos)
                        if self.column1_area.collidepoint(event.pos):
                            self.counter_chosen(1, column1)
                            #print (column1)

                        if self.column2_area.collidepoint(event.pos):
                            self.counter_chosen(2, column2)
            pygame.display.flip()
            fpsControl.tick(60)
        pygame.quit()
        sys.exit()


    def counter_chosen(self, column_destination, column_picked):
        counter = 0
        for x in column_picked:
            if x == 0:
                y_displacement = int(self.displace_y * (10 - counter))
                x_displacement = int(self.displace_x * (column_destination -1))
                #print (x_displacement)
                #print (y_displacement)
                self.screen.blit(player_counter, (x_displacement, y_displacement))
                column_picked[counter] = 1
                break
            counter = counter + 1
                

app()
