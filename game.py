import sys

import numpy as np
import pygame
from pygame.locals import QUIT, K_ESCAPE, K_SPACE, K_RETURN

# Screen settings
screen_size = 480
board_size = 400
square_size = 40
dims = int(board_size/square_size)
game_board = np.zeros((dims, dims))
color = (70,70,70)

button_color_play_out = (0,100,0)
button_color_play_in = (0,255,0)

button_color_pause_out = (100,0,0)
button_color_pause_in = (255,0,0)

text_color = (255,255,255)
text = ' Start  '
clear = '  Clear  '
step_text = '  Step  '
update_game = False


# Pygame init
pygame.init()
pygame.display.set_caption('Game of Life!!')
screen = pygame.display.set_mode((board_size, screen_size))
font = pygame.font.SysFont('Verdana', 30)
# Play button
button_play = font.render(text, True, text_color, button_color_play_out)
button_play_pos = (10, 420)
# Clear button
button_clear = font.render(clear, True, text_color, button_color_pause_out)
button_clear_pos = (135, 420)
# Step button
button_step = font.render(step_text, True, text_color, button_color_play_out)
button_step_pos = (275, 420)
# Clock
clock = pygame.time.Clock()

in_play_button = lambda x,y: 120 >= x >= 9 and 460 >= y >= 420
in_clear_button = lambda x,y: 257 >= x >= 135 and 460 >= y >= 420
in_step_button = lambda x,y: 388 >= x >= 275 and 460 >= y >= 420

def step(update_game:bool):
    global game_board
    # Draw grid
    state = np.copy(game_board)
    for y in range(0, board_size-1, square_size):
        for x in range(0, board_size-1, square_size):

            _x = int(x/square_size)
            _y = int(y/square_size)

            if update_game:
                life_cells = \
                    state[(_y - 1) % dims, (_x - 1) % dims] + \
                    state[(_y - 1) % dims,  _x      % dims] + \
                    state[(_y - 1) % dims, (_x + 1) % dims] + \
                    state[ _y      % dims, (_x - 1) % dims] + \
                    state[ _y      % dims, (_x + 1) % dims] + \
                    state[(_y + 1) % dims, (_x - 1) % dims] + \
                    state[(_y + 1) % dims,  _x      % dims] + \
                    state[(_y + 1) % dims, (_x + 1) % dims]

                # Rules
                if game_board[_y, _x] == 0 and life_cells == 3:
                    game_board[_y, _x] = 1

                elif game_board[_y, _x] == 1 and (life_cells > 3 or life_cells < 2):
                    game_board[_y, _x] = 0

            # Draw cells
            if game_board[_y,_x] == 0:
                pygame.draw.rect(screen, color, (x, y, square_size, square_size), 1)
            else:
                pygame.draw.rect(screen, color, (x, y, square_size, square_size), 0)


while True:

    clock.tick(30)

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Key pressed
        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            update_game = not update_game
            if update_game:
                text = ' Pause '
            else:
                text = ' Start  '
        elif keys[K_RETURN]:
            step(True)
        elif keys[K_ESCAPE]:
            pygame.quit()
            sys.exit()

        # Mouse pressed
        clicks = pygame.mouse.get_pressed()
        x_pos, y_pos = pygame.mouse.get_pos()
        if sum(clicks) > 0:
            x_cell = int(np.floor(x_pos/square_size))
            y_cell = int(np.floor(y_pos/square_size))
            if y_cell < dims:
                if clicks == (1,0,0):
                    game_board[y_cell, x_cell] = 1
                elif clicks == (0,0,1):
                    game_board[y_cell, x_cell] = 0
            elif in_play_button(x_pos, y_pos):
                update_game = not update_game
                if update_game:
                    text = ' Pause '
                else:
                    text = ' Start  '
            elif in_clear_button(x_pos, y_pos):
                game_board = np.zeros((dims, dims))
            elif in_step_button(x_pos, y_pos):
                step(True)

        # Mouse moving
        if in_play_button(x_pos, y_pos):
            if update_game:
                button_play = font.render(text, True, text_color, button_color_pause_in)
            else:
                button_play = font.render(text, True, text_color, button_color_play_in)
        else:
            if update_game:
                button_play = font.render(text, True, text_color, button_color_pause_out)
            else:
                button_play = font.render(text, True, text_color, button_color_play_out)

        if in_clear_button(x_pos, y_pos):
            button_clear = font.render(clear, True, text_color, button_color_pause_in)
        else:
            button_clear = font.render(clear, True, text_color, button_color_pause_out)

        if in_step_button(x_pos, y_pos):
            button_step = font.render(step_text, True, text_color, button_color_play_in)
        else:
            button_step = font.render(step_text, True, text_color, button_color_play_out)


    screen.fill((40,40,40))

    # Buttons
    screen.blit(button_play, button_play_pos)
    screen.blit(button_clear, button_clear_pos)
    screen.blit(button_step, button_step_pos)

    step(update_game)

    pygame.display.flip()
