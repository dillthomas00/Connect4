import pygame
import sys
import random
import time
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
player_counter = pygame.image.load(".//Assets//player_counter.png")
player_counter = pygame.transform.scale(player_counter, (80, 75))
computer_counter = pygame.image.load(".//Assets//computer_counter.png")
computer_counter = pygame.transform.scale(computer_counter, (80, 75))

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
        grid = pygame.image.load(".//Assets//gridtester.png")
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
                            pos_x, posy = event.pos
                            row_picked = int((pos_x - 410) / 98) # column is vertical, row is horizontal
                            self.counter_place(row_picked)
                            self.computer_move() #AI's Turn
                                
            pygame.display.flip()
            fpsControl.tick(60)
        pygame.quit()
        sys.exit()

    def counter_place(self, row_picked):            
        if self.player_turn == True:
            player_counter_numerator = 1
            counter_type = player_counter
            self.player_turn = False
        else:
            player_counter_numerator = 2
            counter_type = computer_counter
            self.player_turn = True   
        counter = row_count -1   
        for x in board:
            if board[counter][row_picked] == 0:
                column_picked = counter
                board[column_picked][row_picked]= player_counter_numerator
                x_displacement = self.starting_x + (self.displace_x * row_picked)
                y_displacement = self.starting_y  + (self.displace_y * column_picked)
                self.counter_animation(x_displacement, y_displacement, counter_type)
                self.winner_check(player_counter_numerator)
                break
            else:
                counter = counter - 1

    def counter_animation(self, x_displacement, y_displacement, counter_type):
        counter = 0
        animation_displacement = y_displacement / 50
        current_y_pos = 125 + (counter * animation_displacement)
        while current_y_pos < y_displacement:
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(counter_type, (x_displacement, current_y_pos))
            pygame.display.update()
            counter = counter + 1
            current_y_pos = 125 + (counter * animation_displacement)
        self.background.blit(counter_type, (x_displacement, y_displacement))
        self.screen.blit(self.background, (0,0))

    def winner_check(self,  counter_numerator) :
        for c in range(column_count-3): #Horizontal
                for r in range(row_count):
                        if board[r][c] == counter_numerator and board[r][c+1] == counter_numerator and board[r][c+2] == counter_numerator and board[r][c+3] == counter_numerator:
                            print ("Player" + str(counter_numerator) +  " has won")
                            return True
        for c in range(column_count): #Vertical
                for r in range(row_count-3):
                        if board[r][c] == counter_numerator and board[r+1][c] == counter_numerator and board[r+2][c] == counter_numerator and board[r+3][c] == counter_numerator:
                            print ("Player" + str(counter_numerator) +  " has won")
                            return True
        for c in range(column_count-3): #Positive Diagional
                for r in range(row_count-3):
                        if board[r][c] == counter_numerator and board[r+1][c+1] == counter_numerator and board[r+2][c+2] == counter_numerator and board[r+3][c+3] == counter_numerator:
                            print ("Player" + str(counter_numerator) +  " has won")
                            return True
        for c in range(column_count-3): #Negative Digional
                for r in range(3, row_count):
                        if board[r][c] == counter_numerator and board[r-1][c+1] == counter_numerator and board[r-2][c+2] == counter_numerator and board[r-3][c+3] == counter_numerator:
                            print ("Player" + str(counter_numerator) +  " has won")
                            return True
        return False

    def valid_locations_check(self):
        valid_locations = []
        for r in range(row_count):
            for c in range(column_count): #Horizontal
                if board[r][c] == 0:
                    valid_locations.append(str(r) + ":" + str(c))
                    try:
                        obselete_location = str(r-1) + ":" + str(c)
                        valid_locations.remove(obselete_location)
                    except:
                        pass
        return valid_locations


    def computer_move(self):
        computer_counter = 0
        best_moves, priority_move, scores = self.get_potential_moves(board)
        if priority_move == True:
            best_move = best_moves[-1]
        else:
            best_move = random.choice(best_moves)
            highest_score = 0
            higest_score_counter = 0
            counter = 0
##            for x in best_moves: ##Unimplemented score checker --- Logic is sound --- Just requires the scoring and potential winning check functions
##                if x > highest_score:
##                    highest_score = x
##                    highest_score_counter = counter
##                counter = counter + 1
##              x = int(best_move[highest_score_counter])                    
                
        x = int(best_move[2:])
        print (x)
        self.counter_place(x)        


    def get_potential_moves(self, current_board):
        player_counter = 1
        computer_counter = 0
        # Figure out the best move to make.
        valid_locations = self.valid_locations_check()
        best_moves = []
        scores = []
        priority_move = False
        for player_move in valid_locations:
            dupe_board = copy.deepcopy(current_board)
            result = self.make_move_attempt(dupe_board, player_move, 2) #Do a score up-count for whatever is in the dupe board
            if result == True:
                print ("Problematic winning move")
                best_moves.append(player_move)
                priority_move = True
                break
            else:
                # do other player's moves and determine best one that they will likely make
                for enemy_move in valid_locations:
                    dupe_board2 = copy.deepcopy(dupe_board)
                    result = self.make_move_attempt(dupe_board2, player_move, 1)
                    if result == True:
                        best_moves.append(player_move)
                        priority_move = True
                        break
                    else:
                        best_moves.append(player_move)
        return best_moves, priority_move, scores 



    def make_move_attempt(self, dupeboard, playerMove, counter):
        x = int(playerMove[0])
        y = int(playerMove[2:])
        dupeboard[x][y] = counter
        result = self.winner_check(counter) #Pretty sure the problem is the logic of the winner check so i will need a seperate winner possble check which will take in the player's move
        return result

   
app()
