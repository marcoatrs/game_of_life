from os import name, system

import numpy as np

def clear_screen():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


class game_of_life:
    __slots__ = (['game_board', 'rc', 'cc'])

    def __init__(self, rows_count:int=20, col_count:int=20, init_state:bool=True):

        self.rc = int(rows_count)
        self.cc = int(col_count)
        self.game_board = np.zeros((self.rc, self.cc), dtype=np.int16)

        # Game init state
        if init_state:
            self.game_board[ 9, 10] = 1
            self.game_board[10, 11] = 1
            self.game_board[11,  9] = 1
            self.game_board[11, 10] = 1
            self.game_board[11, 11] = 1

    def __call__(self):

        state = np.copy(self.game_board)

        for y in range(self.rc):
            for x in range(self.cc):

                life_cells = \
                    state[(x - 1) % self.cc, (y - 1) % self.rc] + \
                    state[(x - 1) % self.cc,  y      % self.rc] + \
                    state[(x - 1) % self.cc, (y + 1) % self.rc] + \
                    state[ x      % self.cc, (y - 1) % self.rc] + \
                    state[ x      % self.cc, (y + 1) % self.rc] + \
                    state[(x + 1) % self.cc, (y - 1) % self.rc] + \
                    state[(x + 1) % self.cc,  y      % self.rc] + \
                    state[(x + 1) % self.cc, (y + 1) % self.rc]

                # Rules
                if self.game_board[x, y] == 0 and life_cells == 3:
                    self.game_board[x, y] = 1

                elif self.game_board[x, y] == 1 and (life_cells > 3 or life_cells < 2):
                    self.game_board[x, y] = 0

        return self.game_board

    def __repr__(self):

        repr = str(self.game_board).replace("0", " ").replace("1", "o")
        repr = repr.replace("[", "").replace("]", "").replace(".", " ")
        return repr

if __name__ == '__main__':
    game = game_of_life()
    exit = ''

    while exit != 'exit':

        clear_screen()
        print(game)
        game()
        exit = input()
