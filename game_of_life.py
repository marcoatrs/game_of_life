import sys

import numpy as np
import pygame
from pygame.locals import QUIT, K_ESCAPE, K_SPACE, K_RETURN

pygame.init()
font = pygame.font.SysFont('Verdana', 30)
bg = (40,40,40)
lines = (70,70,70)
white = (255,255,255)

in_play_button = lambda x,y: 120 >= x >= 9 and 645 >= y >= 605
in_clear_button = lambda x,y: 257 >= x >= 135 and 645 >= y >= 605
in_step_button = lambda x,y: 388 >= x >= 275 and 645 >= y >= 605

class button:
    __slots__ = (['main_text', 'second_text','main_color', 'select_color', 'pos'])
    def __init__(self, main_text:str='', second_text:str='', main_color:tuple=(0,100,0), select_color:tuple=(0,255,0), pos:tuple=(0,0)):
        self.main_text = main_text
        self.second_text = second_text
        self.main_color = main_color
        self.select_color = select_color
        self.pos = pos

    def __call__(self, text:bool=True, color:bool=True):
        if text:
            _text = self.main_text
        else:
            _text = self.second_text
        if color:
            _color = self.main_color
        else:
            _color = self.select_color

        return font.render(_text, True, white, _color)



class game_of_life():

    def __init__(self):

        self.width = 1200
        self.height = 600
        self.square_size = 15

        self.rc = int(self.height / self.square_size)
        self.cc = int(self.width / self.square_size)

        self.game_board = np.zeros((self.rc, self.cc))

        # Buttons
        self.play_button = button(' Start  ', ' Pause ', (0,100,0), (0,255,0), (10, 605))
        self.clear_button = button('  Clear  ', '', (100,0,0), (255,0,0), (135, 605))
        self.step_button = button('  Step  ', '', (0,100,0), (0,255,0), (275, 605))

        pygame.init()
        pygame.display.set_caption('Game of Life!!')
        self.screen = pygame.display.set_mode((self.width, self.height + 60))
        self.clock = pygame.time.Clock()
        self.update_game = False

    def __call__(self, update_game:bool=False):

        state = np.copy(self.game_board)

        for row in range(self.rc):
            for col in range(self.cc):

                if update_game:

                    life_cells = \
                        state[(row - 1) % self.rc, (col - 1) % self.cc] + \
                        state[(row - 1) % self.rc,  col      % self.cc] + \
                        state[(row - 1) % self.rc, (col + 1) % self.cc] + \
                        state[ row      % self.rc, (col - 1) % self.cc] + \
                        state[ row      % self.rc, (col + 1) % self.cc] + \
                        state[(row + 1) % self.rc, (col - 1) % self.cc] + \
                        state[(row + 1) % self.rc,  col      % self.cc] + \
                        state[(row + 1) % self.rc, (col + 1) % self.cc]

                    # Rules
                    if self.game_board[row, col] == 0 and life_cells == 3:
                        self.game_board[row, col] = 1

                    elif self.game_board[row, col] == 1 and (life_cells > 3 or life_cells < 2):
                        self.game_board[row, col] = 0

                # Draw cells
                if self.game_board[row, col] == 0:
                    pygame.draw.rect(self.screen, lines, (col * self.square_size, row * self.square_size, self.square_size, self.square_size), 1)
                else:
                    pygame.draw.rect(self.screen, white, (col * self.square_size, row * self.square_size, self.square_size, self.square_size), 0)

    def events(self):

        for event in pygame.event.get():

            keys = pygame.key.get_pressed()
            clicks = pygame.mouse.get_pressed()
            x_pos, y_pos = pygame.mouse.get_pos()

            # Close game
            if event.type == QUIT or keys[K_ESCAPE]:
                pygame.quit()
                sys.exit()

            # Play / Pause game
            elif keys[K_SPACE] or (clicks == (1,0,0) and in_play_button(x_pos, y_pos)):
                self.update_game = not self.update_game

            # Clear game
            elif clicks == (1,0,0) and in_clear_button(x_pos, y_pos):
                self.game_board = np.zeros((self.rc, self.cc))

            # Game Step
            elif keys[K_RETURN] or (clicks == (1,0,0) and in_step_button(x_pos, y_pos)):
                self(True)

            # Clicks events
            if sum(clicks) > 0:
                x_cell = int(np.floor(x_pos/self.square_size))
                y_cell = int(np.floor(y_pos/self.square_size))

                if y_cell < self.rc:
                    # Revive cell
                    if clicks == (1,0,0):
                        self.game_board[y_cell, x_cell] = 1
                    # Kill cell
                    elif clicks == (0,0,1):
                        self.game_board[y_cell, x_cell] = 0

            # Mouse moving
            self.pb = self.play_button(not self.update_game, not in_play_button(x_pos, y_pos))
            self.cb = self.clear_button(True, not in_clear_button(x_pos, y_pos))
            self.sb = self.step_button(True, not in_step_button(x_pos, y_pos))

        self.screen.blit(self.pb, self.play_button.pos)
        self.screen.blit(self.cb, self.clear_button.pos)
        self.screen.blit(self.sb, self.step_button.pos)


game = game_of_life()

while True:

    game.clock.tick(30)
    game.screen.fill(bg)
    game.events()
    game(game.update_game)
    pygame.display.flip()
