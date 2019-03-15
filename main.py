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
# Image Asset
player_counter = pygame.image.load(".//Assets//player_counter.png")
player_counter = pygame.transform.scale(player_counter, (80, 75))
computer_counter = pygame.image.load(".//Assets//computer_counter.png")
computer_counter = pygame.transform.scale(computer_counter, (80, 75))


### Start Menu of Connect4
class start_menu():
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.animation_state = 0
        self.x_axis = -1
        self.y_axis = 10
        self.main()

    def main(self):
        grid = pygame.image.load(".//Assets//grid.png")
        grid = pygame.transform.scale(grid, (1280, 900))
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((255,255,255))
        self.background.blit(grid, (510, 50)) 
        self.screen.blit(self.background, (0,0))
        game_menu = pygame.image.load(".//Assets//game_menu.png")
        self.screen.blit(game_menu, (100, 25))

        self.instruction_state_boolean = False
        instructions_state = 1
        x1, x2, y1, y2 = 140, 500, 320, 410
        self.play_area = pygame.Rect(x1, y1, (x2-x1), (y2-y1))
        y1, y2 = 440, 530
        self.play_area_2 = pygame.Rect(x1, y1, (x2-x1), (y2-y1))
        y1, y2 = 560, 650
        self.instructions_area = pygame.Rect(x1, y1, (x2-x1), (y2-y1))
        y1, y2 = 820, 920      
        self.exit_area = pygame.Rect(x1, y1, (x2-x1), (y2-y1))
        self.instruction_exit_area = pygame.Rect(0, 0, 0, 0)
        self.backwards_area = pygame.Rect(0, 0, 0, 0)
        self.forwards_area = pygame.Rect(0, 0, 0, 0)
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button.
                        if self.play_area.collidepoint(event.pos):
                            app(2)
                        if self.play_area_2.collidepoint(event.pos):
                            app(1)
                        elif self.instructions_area.collidepoint(event.pos):
                            instructions_state = self.instructions(
                                instructions_state)  
                        elif self.backwards_area.collidepoint(event.pos):
                            instructions_state = self.instructions_update(
                                instructions_state, -1)
                        elif self.forwards_area.collidepoint(event.pos):
                            instructions_state = self.instructions_update(
                                instructions_state, 1)
                        elif self.instruction_exit_area.collidepoint(event.pos):
                            self.main()
                        elif self.exit_area.collidepoint(event.pos):
                            done = True

            self.menu_animation(game_menu)
            self.screen.blit(game_menu, (0, 0))
            try:
                if self.instruction_state_boolean == True:
                    self.screen.blit(self.instructions_menu,
                                     (int(screen_width / 3.75), 200))
            except:
                pass
            pygame.display.flip()
            fpsControl.tick(60)
        pygame.quit()
        sys.exit()

    def menu_animation(self, game_menu):
        if self.animation_state < 110:
            if self.animation_state % 2 == 1:
                counter = pygame.image.load(".//Assets//player_counter.png")
                counter = pygame.transform.scale(counter, (80, 75))
            else:
                counter = pygame.image.load(".//Assets//computer_counter.png")
                counter = pygame.transform.scale(counter, (80, 75))
            if self.animation_state % 11 == 0:
                self.y_axis = self.y_axis - 1
                self.x_axis = -1
            else:
                self.x_axis = self.x_axis + 1
            x  = 720
            y = 175
            displace_x = 97.5
            displace_y = 77.5
            x = x + (displace_x * (self.x_axis))
            y = y + (displace_y * (self.y_axis))
            self.background.blit(counter, (x, y))
            self.screen.blit(self.background, (0, 0))
            self.animation_state = self.animation_state + 1
        else:
            grid = pygame.image.load(".//Assets//grid.png")
            grid = pygame.transform.scale(grid, (1280, 900))
            self.background = pygame.Surface(self.screen.get_size())
            self.background = self.background.convert()
            self.background.fill((255,255,255))
            self.background.blit(grid, (510, 50)) 
            self.screen.blit(self.background, (0,0))
            self.animation_state = 0
            self.x_axis = -1
            self.y_axis = 10

    def instructions(self, instructions_state):
        self.instruction_state_boolean = True
        self.instructions_menu = pygame.image.load(
            ".//Assets//instructions_" + str(instructions_state) + ".png")
        x1, y1, x2, y2 = 845, 800, 1135, 850  # Exit
        self.instruction_exit_area = pygame.Rect(x1, y1, (x2-x1), (y2-y1))
        x1, y1, x2, y2 = 1160, 800, 1200, 850  # back one
        self.backwards_area = pygame.Rect(x1, y1, (x2-x1), (y2-y1))
        x1, y1, x2, y2 = 1280, 800, 1320, 850  # forward one
        self.forwards_area = pygame.Rect(x1, y1, (x2-x1), (y2-y1))
        return instructions_state

    def instructions_update(self, instructions_state, instructions_position):
        try:
            self.instructions_menu = pygame.image.load(
                ".//Assets//instructions_" + str(instructions_state + instructions_position) + ".png")
            instructions_state = instructions_state + instructions_position
        except pygame.error:
            self.instructions_menu = pygame.image.load(
                ".//Assets//instructions_" + str(instructions_state) + ".png")
        return instructions_state





### Main Application
class app():
    def __init__(self, gamemode):
        self.gamemode = gamemode
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.starting_x  = 420
        self.starting_y = 125
        self.displace_x = 98
        self.displace_y = 77.5
        self.player_turn = True
        self.main()

    def main(self):
        self.board = numpy.zeros((row_count, column_count))
        grid = pygame.image.load(".//Assets//grid.png")
        grid = pygame.transform.scale(grid, (1280, 900))
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((255,255,255))
        self.background.blit(grid, (310, 0)) #(1920 - 1280) / 2
        back_button  = pygame.image.load(".//Assets//back_button.png")
        pygame.transform.scale(back_button, (400, 100))
        self.background.blit(back_button, (790, 910))
        self.screen.blit(self.background, (0,0))

        x1, y1, x2, y2 = 410, 130, 1521, 900
        self.column_area = pygame.Rect(x1, y1, (x2-x1), (y2-y1))
        x1, y1, x2, y2 = 790, 910, 1100, 990
        self.back_button_area = pygame.Rect(x1, y1, (x2-x1), (y2-y1))
        self.play_again_area = pygame.Rect(0,0,0,0)
        self.exit_area = pygame.Rect(0,0,0,0)
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
                            result = self.winner_check(self.board, 1)
                            if result == True:
                                self.winner_route(1)
                            else:
                                if self.gamemode == 2:
                                    self.computer_move() #AI's Turn
                                result = self.winner_check(self.board, 2)
                                if result == True:
                                    self.winner_route(2)
                        elif self.back_button_area.collidepoint(event.pos):
                            start_menu()
                        elif self.play_again_area.collidepoint(event.pos):
                            self.board = numpy.zeros((row_count, column_count))
                            self.__init__(self.gamemode)
                        elif self.exit_area.collidepoint(event.pos):
                            done = True
                            start_menu() 
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
        for x in self.board:
            if self.board[counter][row_picked] == 0:
                column_picked = counter
                self.board[column_picked][row_picked]= player_counter_numerator
                x_displacement = self.starting_x + (self.displace_x * row_picked)
                y_displacement = self.starting_y  + (self.displace_y * column_picked)
                self.counter_animation(x_displacement, y_displacement, counter_type)
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

    def winner_check(self, board, counter_numerator):
        for c in range(column_count-3): #Horizontal
                for r in range(row_count):
                        if self.board[r][c] == counter_numerator and board[r][c+1] == counter_numerator and board[r][c+2] == counter_numerator and board[r][c+3] == counter_numerator:
                            return True
        for c in range(column_count): #Vertical
                for r in range(row_count-3):
                        if board[r][c] == counter_numerator and board[r+1][c] == counter_numerator and board[r+2][c] == counter_numerator and board[r+3][c] == counter_numerator:
                            return True
        for c in range(column_count-3): #Positive Diagional
                for r in range(row_count-3):
                        if board[r][c] == counter_numerator and board[r+1][c+1] == counter_numerator and board[r+2][c+2] == counter_numerator and board[r+3][c+3] == counter_numerator:
                            return True
        for c in range(column_count-3): #Negative Digional
                for r in range(3, row_count):
                        if board[r][c] == counter_numerator and board[r-1][c+1] == counter_numerator and board[r-2][c+2] == counter_numerator and board[r-3][c+3] == counter_numerator:
                            return True
        return False

    def valid_locations_check(self):
        valid_locations = []
        for r in range(row_count):
            for c in range(column_count): #Horizontal
                if self.board[r][c] == 0:
                    valid_locations.append(str(r) + ":" + str(c))
                    try:
                        obselete_location = str(r-1) + ":" + str(c)
                        valid_locations.remove(obselete_location)
                    except:
                        pass
        return valid_locations


    def computer_move(self):
        computer_counter = 0
        best_moves, priority_move, scores = self.get_potential_moves(self.board)
        if priority_move == True:
            counter = 0
            best_move = best_moves[-1]
        else:
            best_move = random.choice(best_moves)
            highest_score = 0
            higest_score_counter = 0
            counter = 0
        x = int(best_move[2:])
        self.counter_place(x)        


    def get_potential_moves(self, current_board):
        player_counter = 1
        computer_counter = 0
        # Figure out the best move to make.
        valid_locations = self.valid_locations_check()
        best_moves = []
        scores = []
        priority_move = False
        for computer_move in valid_locations:
            dupe_board = copy.deepcopy(current_board)
            result = self.make_move_attempt(dupe_board, computer_move, 2) #Do a score up-count for whatever is in the dupe self.board
            if result == True:
                best_moves.append(computer_move)
                priority_move = True
                break
            else:
                # do other player's moves and determine best one that they will likely make
                for enemy_move in valid_locations:
                    dupe_board2 = copy.deepcopy(dupe_board)
                    result = self.make_move_attempt(dupe_board2, enemy_move, 1)
                    if result == True:
                        best_moves.append(enemy_move)
                        priority_move = True
                        break
                    else:
                        best_moves.append(enemy_move)
        return best_moves, priority_move, scores 


    def make_move_attempt(self, dupeboard, playerMove, counter):
        x = int(playerMove[2:])
        y = int(playerMove[0])
        dupeboard[y][x] = counter
        result = self.winner_check(dupeboard, counter) #Pretty sure the problem is the logic of the winner check so i will need a seperate winner possble check which will take in the player's move
        return result

    def winner_route(self, counter_numerator):
        winner_screen = pygame.image.load(".//Assets//player_" + str(counter_numerator) + "_winner.png")
        self.screen.blit(winner_screen, (632, 213))
        x1, y1, x2, y2 = 810, 550, 1090, 620
        self.play_again_area = pygame.Rect(x1, y1, (x2-x1), (y2-y1))
        x1, y1, x2, y2 =  810, 650, 1090, 720
        self.exit_area = pygame.Rect(x1, y1, (x2-x1), (y2-y1))
        self.column_area = pygame.Rect(0,0,0,0)
        self.back_button_area = pygame.Rect(0,0,0,0)


start_menu()
