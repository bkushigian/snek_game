''' 
This is the board class. Currently not an optimal implementation. I will be
trying to update after I get the game working.
'''
import os
from sys import exit
from externs import *



class Board(object):
    ''' Board Class: To use board:
        1) Create it: b = Board()
        2) Load level: b.load_level(1)
        3) Init Snake
    '''
    def __init__(self, level = None, score = 0, screen = None):

        self.level = level
        self.lives = 3
        self.snake = [[2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6]]

        self.score          = score

        self.name           = ''
        self.sleepTime      = 0.25
        self.applePoints    = 0
        self.moneyPoints    = 0
        self.hint           = ''

        self.screen = screen
        self.current_direction = RIGHT

        if self.level:
            self.load_level(self.level)

    def load_level(self, levelNumber):
        self.level = levelNumber
        level      = os.path.join('data', 'lv{}.txt'.format(levelNumber))
        try:
            with open(level, 'r') as f:
                lines = f.readlines()
        except:
            # TODO: Handle ncurses, release screen
            print "Could not open level", level
            exit(1)

        # Load the actual board
        self.board = [line[:-1] for line in lines[:BOARD_HEIGHT]]

        # Get info for level, such as name and sleep time.
        for line in lines[BOARD_HEIGHT:]:
            if line.startswith('name'):
                self.name = line.split('=')[1][:-1]
            elif line.startswith('sleep'):
                self.sleepTime = float(line.split('=')[1])
            elif line.startswith('appt'):
                self.applePoints = int(line.split('=')[1])
            elif line.startswith('mnpt'):
                self.moneyPoints = int(line.split('=')[1])
            elif line.startswith('text'):
                self.hint = line.split('=')[1][:-1]
            else:
                continue
    def init_snake(self):
        self.snake = [(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6)]

    def move(self):
        ''' Move in current_direction. '''
        head = self.snake[-1]
        direction = self.current_direction
        if direction == UP:
            new_head = (head[0] - 1, head[1])
        elif direction == DOWN:
            new_head = (head[0] + 1, head[1])
        elif direction == LEFT:
            new_head = (head[0], head[1] - 1)
        elif direction == RIGHT:
            new_head = (head[0], head[1] + 1)

        self.snake = (self.snake[1:]).append(new_head)
        self.check_position()     # This checks if a) we have died, b) if we won

    def check_position(self):
        '''
        Checks position, returns True if position is valid,
        False on game over
        '''
        # First, check head for self-intersection
        y,x = head = self.snake[-1]
        for pos in self.snake[:-1]:
            if pos == head:
                return False

        # Then check against blocks
        if self.is_dangerous(head):
            return False

        # Now, check for good stuff!
        if self.board[y][x] == APPLE:
            self.eat_apple()

        elif self.board[y][x] == MONEY:
            self.eat_money()

        elif self.board[y][x] == LIFE or self.board[y][x] == SECRETLIFE:
            self.eat_life()

        return True  # Our position is valid, return true


    def eat_apple(self):
        y,x = head = snake[-1]
        if self.board[y][x] != APPLE:
            raise RuntimeError("No apple at position ({},{})".format( y, x))
        self.board[y][x] = SPACE
        self.score += self.applePoints

    def eat_money(self):
        y,x = head = snake[-1]
        if self.board[y][x] != MONEY:
            raise RuntimeError("No money at position ({},{})".format( y, x))
        self.board[y][x] = SPACE
        self.score += self.moneyPoints

    def eat_life(self):
        y,x = head = snake[-1]
        if self.board[y][x] != LIFE and self.board[y][x] != SECRETLIFE:
            raise RuntimeError("No life at position ({},{})".format( y, x))
        self.board[y][x] = SPACE
        if self.board[y][x] == SECRETLIFE:
            self.board[y][x] = SECRET
        self.lives += 1
        


    def game_over(self):
        # TODO
        pass

    def is_dangerous(self, pos):
        '''
        pos: tuple (y,x)
        return true if pos (y,x) on self.board is a dangerous tile (such as a
        block
        '''
        return self.board(pos[0], pos[1]) in (BLOCK,)

# For Testing
b = Board(1)
