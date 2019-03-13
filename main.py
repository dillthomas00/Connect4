import pygame
import sys
import random
import time
import numpy 

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
                            self.computer_evaluate()
                                
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
                self.winner_check(column_picked, row_picked, player_counter_numerator)
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

    def winner_check(self, column_picked, row_picked, counter_numerator) :
        for c in range(column_count-3): #Horizontal
                for r in range(row_count):
                        if board[r][c] == counter_numerator and board[r][c+1] == counter_numerator and board[r][c+2] == counter_numerator and board[r][c+3] == counter_numerator:
                            print ("Player" + str(counter_numerator) +  " has won")
        for c in range(column_count): #Vertical
                for r in range(row_count-3):
                        if board[r][c] == counter_numerator and board[r+1][c] == counter_numerator and board[r+2][c] == counter_numerator and board[r+3][c] == counter_numerator:
                            print ("Player" + str(counter_numerator) +  " has won")
        for c in range(column_count-3): #Positive Diagional
                for r in range(row_count-3):
                        if board[r][c] == counter_numerator and board[r+1][c+1] == counter_numerator and board[r+2][c+2] == counter_numerator and board[r+3][c+3] == counter_numerator:
                            print ("Player" + str(counter_numerator) +  " has won")
        for c in range(column_count-3): #Negative Digional
                for r in range(3, row_count):
                        if board[r][c] == counter_numerator and board[r-1][c+1] == counter_numerator and board[r-2][c+2] == counter_numerator and board[r-3][c+3] == counter_numerator:
                            print ("Player" + str(counter_numerator) +  " has won")

    def computer_evaluate(self):
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
        column_picked, row_picked = self.best_move(valid_locations)
        print (column_picked, row_picked)
        self.counter_place(column_picked)

                    
    def best_move(self, valid_locations):
        print (valid_locations)
        best_score = -10000
        best_col = random.choice(valid_locations)
        best_row = 0
        for x in valid_locations:
            row = int(x[0])
            column = int(x[2:])
            temp_board = board.copy()
            score = self.temp_drop(temp_board, row, column, valid_locations)
            if score > best_score:
                best_score = score
                best_column = column
                best_row = row
        return best_column, row
            

    def temp_drop(self, temp_board, row, column, valid_locations):
        computer_counter = 2
        temp_board[row][column] = computer_counter
        score = 0
        center_array = [int(i) for i in list(board[:, row_count //2])]
        center_count = center_array.count(computer_counter)
        score += center_count * 3
        
        ## Score Horizontal
        for r in range(row_count):
                row_array = [int(i) for i in list(board[r,:])]
                for c in range(column_count-3):
                        window = row_array[c:c+4]
                        score += self.evaluate_window(window)

        ## Score Vertical
        for c in range(column_count):
                col_array = [int(i) for i in list(board[:,c])]
                for r in range(row_count-3):
                        window = col_array[r:r+4]
                        score += self.evaluate_window(window)

        ## posiive sloped diagonal
        for r in range(row_count-3):
                for c in range(column_count-3):
                        window = [board[r+i][c+i] for i in range(4)]
                        score += self.evaluate_window(window)
        ## 
        for r in range(row_count-3):
                for c in range(column_count-3):
                        window = [board[r+3-i][c+i] for i in range(4)]
                        score += self.evaluate_window(window)
        return score

    def evaluate_window(self, window):
        score = 0
        empty = 0
        computer_piece = 2
        player_piece = 1

        # Horizontal
        for r in range(row_count):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(column_count - 3):
                window = row_array[c : c + 4]
                if window.count(computer_piece) == 4:
                    score = score + 100
                elif window.count(computer_piece) ==3 and window.count(empty) == 1:
                    score = score + 100

            # Vertical
            for c in range(column_count):
                col_array = [int(i) for i in list(board[:, c])]
                for r in range(row_count - 3):
                    window = col_array[r : r + 4]
                    if window.count(computer_piece) == 4:
                        score = score + 100
                    elif window.count(computer_piece) == 3 and window.count(empty) == 1:
                        score = score + 10

            # Positive diagonal
            for r in range(row_count - 3):
                for c in range(column_count - 3):
                    window = [board[r+i][c+i] for i in range(4)]
                    if window.count(computer_piece) == 4:
                        score = score + 100
                    elif window.count(computer_piece) == 3 and window.count(empty) == 1:
                        score = score + 10

            # Negative diagonal
            for r in range(row_count - 3):
                for c in range(column_count - 3):
                    window = [board[r+i][c+i] for i in range(4)]
                    if window.count(computer_piece) == 4:
                        score = score + 100
                    elif window.count(computer_piece) == 3 and window.count(empty) == 1:
                        score = score + 10
                        
            return score
                    

   
app()
