import sys

import numpy as np
import pygame
from pygame.locals import (K_ESCAPE, K_RETURN, K_SPACE, KEYDOWN,
                           MOUSEBUTTONDOWN, MOUSEMOTION, QUIT)

pygame.init()
font = pygame.font.SysFont('Verdana', 30)
bg = (40, 40, 40)
lines = (70, 70, 70)
white = (255, 255, 255)

in_play_button = lambda x, y: 120 >= x >= 9 and 645 >= y >= 605
in_clear_button = lambda x, y: 257 >= x >= 135 and 645 >= y >= 605
in_step_button = lambda x, y: 388 >= x >= 275 and 645 >= y >= 605


class Button:
    __slots__ = ([
        'main_text', 'second_text', 'main_color', 'select_color', 'pos'
    ])

    def __init__(self,
                 main_text: str = '',
                 second_text: str = '',
                 main_color: tuple = (0, 100, 0),
                 select_color: tuple = (0, 255, 0),
                 pos: tuple = (0, 0)):
        self.main_text = main_text
        self.second_text = second_text
        self.main_color = main_color
        self.select_color = select_color
        self.pos = pos

    def __call__(self, text: bool = True, color: bool = True):
        if text:
            _text = self.main_text
        else:
            _text = self.second_text
        if color:
            _color = self.main_color
        else:
            _color = self.select_color

        return font.render(_text, True, white, _color)


class GameOfLife():

    def __init__(self):

        self.width = 1200
        self.height = 600
        self.square_size = 10

        self.rc = int(self.height / self.square_size)
        self.cc = int(self.width / self.square_size)

        self.game_board = np.zeros((self.rc, self.cc))

        # Buttons
        self.play_button = Button(' Start  ', ' Pause ', (0, 100, 0),
                                  (0, 255, 0), (10, 605))
        self.clear_button = Button('  Clear  ', '', (100, 0, 0), (255, 0, 0),
                                   (135, 605))
        self.step_button = Button('  Step  ', '', (0, 100, 0), (0, 255, 0),
                                  (275, 605))

        pygame.init()
        pygame.display.set_caption('Game of Life!!')
        self.screen = pygame.display.set_mode((self.width, self.height + 60))
        self.clock = pygame.time.Clock()
        self.update_game = False

    def __call__(self, update_game: bool = False):

        state = np.copy(self.game_board)

        for row in range(self.rc):
            for col in range(self.cc):
                if update_game:
                    life_cells = \
                        state[(row - 1) % self.rc, (col - 1) % self.cc] + \
                        state[(row - 1) % self.rc, col % self.cc] + \
                        state[(row - 1) % self.rc, (col + 1) % self.cc] + \
                        state[ row % self.rc, (col - 1) % self.cc] + \
                        state[ row % self.rc, (col + 1) % self.cc] + \
                        state[(row + 1) % self.rc, (col - 1) % self.cc] + \
                        state[(row + 1) % self.rc, col % self.cc] + \
                        state[(row + 1) % self.rc, (col + 1) % self.cc]

                    # Rules
                    if self.game_board[row, col] == 0 and life_cells == 3:
                        self.game_board[row, col] = 1

                    elif self.game_board[row, col] == 1 and (life_cells > 3 or
                                                             life_cells < 2):
                        self.game_board[row, col] = 0

                # Draw cells
                if self.game_board[row, col] == 0:
                    pygame.draw.rect(
                        self.screen, lines,
                        (col * self.square_size, row * self.square_size,
                         self.square_size, self.square_size), 1)
                else:
                    pygame.draw.rect(
                        self.screen, white,
                        (col * self.square_size, row * self.square_size,
                         self.square_size, self.square_size), 0)

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def switch_update(self):
        self.update_game = not self.update_game
        self.pb = self.play_button(not self.update_game, True)

    def clear_screen(self):
        self.game_board = np.zeros((self.rc, self.cc))
        if self.update_game:
            self.switch_update()

    def events(self):
        for event in pygame.event.get():

            # Close game
            if event.type == QUIT:
                self.quit_game()

            elif event.type == KEYDOWN:
                keys = pygame.key.get_pressed()

                if keys[K_ESCAPE]:
                    self.quit_game()
                elif keys[K_SPACE]:
                    self.switch_update()
                elif keys[K_RETURN]:
                    self(True)

            elif event.type == MOUSEMOTION:
                x_pos, y_pos = pygame.mouse.get_pos()

                self.pb = self.play_button(not self.update_game,
                                           not in_play_button(x_pos, y_pos))
                self.cb = self.clear_button(True,
                                            not in_clear_button(x_pos, y_pos))
                self.sb = self.step_button(True,
                                           not in_step_button(x_pos, y_pos))

            clicks = pygame.mouse.get_pressed()
            if sum(clicks) == 0:
                continue
            x_pos, y_pos = pygame.mouse.get_pos()

            x_cell = int(np.floor(x_pos / self.square_size))
            y_cell = int(np.floor(y_pos / self.square_size))

            if clicks == (1, 0, 0):

                if in_play_button(x_pos, y_pos):
                    self.switch_update()
                elif in_clear_button(x_pos, y_pos):
                    self.clear_screen()
                elif in_step_button(x_pos, y_pos):
                    self(True)
                elif y_cell < self.rc:
                    self.game_board[y_cell, x_cell] = 1

            elif clicks == (0, 0, 1):

                if y_cell < self.rc:
                    self.game_board[y_cell, x_cell] = 0

        self.screen.blit(self.pb, self.play_button.pos)
        self.screen.blit(self.cb, self.clear_button.pos)
        self.screen.blit(self.sb, self.step_button.pos)


if __name__ == '__main__':
    game = GameOfLife()
    while True:
        game.clock.tick(15)
        game.screen.fill(bg)
        game.events()
        game(game.update_game)
        pygame.display.flip()
