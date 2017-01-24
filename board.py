''' 
This is the board class. Currently not an optimal implementation. I will be
trying to update after I get the game working.
'''
import os
from sys import exit
from externs import *
from drawable import Drawable
from handler import Handler
from action import *
from random import randrange



class Board(Drawable, Handler):
    ''' Board Class: To use board:
        1) Create it: b = Board()
        2) Load level: b.load_level(1)
        3) Init Snake
    '''
    def __init__(self, level = 0, score = 0, screen = None, game = None, actions = None):

        self.level    = level
        self.lives    = 3
        self.score    = score
        self.snake    = [[2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6]]
        self.snakelen = 6

        self.name           = ''
        self.sleepTime      = 0.25
        self.applePoints    = 5
        self.moneyPoints    = 25
        self.hint           = ''

        self.screen = screen
        self.game   = game

        self.current_direction = RIGHT
        self.number_of_apples  = 0

        self.level_name = "DEFAULT LEVEL NAME. I SHOULD PROBABLY UPDATE THIS"

        if self.level:
            self.load_level(self.level)

        self.actions = actions   # This should be set by the Game instance

    def set_screen(self, screen):
        self.screen = screen

    def set_game(self, game):
        self.game = game

    def set_actions(self, actions):
        self.actions = actions

    def load_blank(self):
        self.load_level('blank')

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
        self.board = [list(line[:-1]) for line in lines[:BOARD_HEIGHT]]

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
        # Count the number of apples
        self.number_of_apples = 0
        for line in self.board:
            for c in line:
                if c == '@':
                    self.number_of_apples += 1
        self.init_snake()
                
    def init_snake(self, row = 1, snakelen = 0):
        self.current_direction = RIGHT
        if snakelen > 0:
            self.snakelen = snakelen
        self.snake = [(row, 1), (row, 2), (row, 3), (row, 4), (row, 5), (row, 6)]
        #self.snake = [ (row, i) for i in range(1, self.snakelen + 1)]

    def move(self, new_dir = None):
        ''' Move in current_direction. '''
        head = self.snake[-1]
        if new_dir != None:
            direction = new_dir
        else:
            direction = self.current_direction
        if direction == UP:
            new_head = (head[0] - 1, head[1])
        elif direction == DOWN:
            new_head = (head[0] + 1, head[1])
        elif direction == LEFT:
            new_head = (head[0], head[1] - 1)
        elif direction == RIGHT:
            new_head = (head[0], head[1] + 1)

        if len(self.snake) >= self.snakelen:
            self.snake = self.snake[1:]
        self.snake.append(new_head)
        return self.check_position()     # This checks if a) we have died, b) if we won
    
    def check_position(self):
        '''
        Checks position, returns True if position is valid,
        False on game over
        '''
        # First, check head for self-intersection
        y,x = head = self.snake[-1]
        for pos in self.snake[:-1]:
            if pos == head:
                return WE_HAVE_DIED

        # Then check against blocks
        if self.is_dangerous(head):
            return WE_HAVE_DIED

        # Now, check for good stuff!
        if self.board[y][x] == APPLE:
            self.eat_apple()
            self.number_of_apples -= 1
            if self.number_of_apples < 1:
                return WE_HAVE_WON
            # TODO: Check if we have won

        elif self.board[y][x] == MONEY:
            self.eat_money()

        elif self.board[y][x] == LIFE or self.board[y][x] == SECRETLIFE:
            self.eat_life()

        return WE_KEEP_PLAYING  # Our position is valid, return true


    def eat_apple(self):
        y,x = head = self.snake[-1]
        if self.board[y][x] != APPLE:
            raise RuntimeError("No apple at position ({},{})".format( y, x))
        self.actions['apple'](y,x)
        self.score += self.applePoints

    def eat_money(self):
        y,x = head = self.snake[-1]
        if self.board[y][x] != MONEY:
            raise RuntimeError("No money at position ({},{})".format( y, x))
        self.actions['money'](y,x)

    def eat_life(self):
        y,x = head = self.snake[-1]
        if self.board[y][x] != LIFE and self.board[y][x] != SECRETLIFE:
            raise RuntimeError("No life at position ({},{})".format( y, x))
        
        self.actions['life'](y,x)

    def hit_block(self):
        y,x = head = self.snake[-1]
        if self.board[y][x] != BLOCK:
            raise RuntimeError("No block at position ({},{})".format( y, x))
        self.actions['block'](y,x)




    def game_over(self):
        # TODO
        self.actions['gameover']()

    def is_dangerous(self, pos):
        '''
        pos: tuple (y,x)
        return true if pos (y,x) on self.board is a dangerous tile (such as a
        block
        '''

        if self.board[pos[0]][pos[1]] in (BLOCK,):
            self.hit_block()
            return True

        return False

    def calculate_topleft(self):
        ''' Calculate where top left of board should be placed given board
        height and board width (globals) and maxy, maxx
        '''
        return (6, self.screen.getmaxyx()[1] / 2 - (BOARD_WIDTH / 2))

    def draw(self):
        # TODO: ensure that we have self.screen defined
        board = self.board
        screen = self.screen

        # Clear the screen
        screen.clear()

        # Draw the scoreboard
        #    First, level name (just a generic string for now)
        y0, x0 = 1, screen.centered_string_x(self.level_name)
        screen.addstr(y0, x0, self.level_name)

        # Then, score board
        scoreboard = 'LEVEL {0: <10} SCORE {1: <12} LIVES {2}'.format(
            self.level, self.score, self.lives)
        y0, x0 = 2, screen.centered_string_x(scoreboard)
        screen.addstr(y0, x0, scoreboard)

        # Draw the board
        y0, x0 = self.calculate_topleft()
        y,x = 0,0
        for line in board:
            for char in line:
                screen.write_board_char(y0 + y, x0 + x, char)
                x += 1
            x = 0
            y += 1

        # Draw the snake
        for y,x in self.snake:
            screen.write_board_char(y0 + y, x0 + x, SNAKEBODY)
        screen.write_board_char(y0 + y, x0 + x, HEADRIGHT)

        # Finally, refresh the screen
        screen.refresh()

    def set_dir_left(self):
        self.current_direction = LEFT

    def set_dir_right(self):
        self.current_direction = RIGHT

    def set_dir_up(self):
        self.current_direction = UP

    def set_dir_down(self):
        self.current_direction = DOWN

    def handle(self, ch):
        if   ch in map(ord, 'ah'):
            self.set_dir_left()
        elif ch in map(ord, 'dl'):
            self.set_dir_right()
        elif ch in map(ord, 'wk'):
            self.set_dir_up()
        elif ch in map(ord, 'sj'):
            self.set_dir_down()
        elif ch in map(ord, 'p' ):         # Pause Game
            self.game.pause()

        # TODO: UNIMPLEMENTED...
        elif ch in map(ord, 'm' ):         # Game Menu
            self.game.in_game_menu()

    def grow_snake(self, amount = 1):
        self.snakelen += 1

    def gen_random_apples(self, n = 3):
        free_spaces = []
        board       = self.board
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == SPACE:
                    free_spaces.append((i,j))

        for it in range(n):
            k = randrange(len(free_spaces))
            i,j = free_spaces[k]
            board[i][j] = APPLE
            free_spaces = free_spaces[:k] + free_spaces[k+1:]

        gen_money_prob = randrange(100)
        if gen_money_prob > 85:
            num = (gen_money_prob - 85) / 4
            for it in range(num):
                k = randrange(len(free_spaces))
                i,j = free_spaces[k]
                board[i][j] = MONEY
                free_spaces = free_spaces[:k] + free_spaces[k+1:]

        gen_life_prob = randrange(100)
        if gen_money_prob > 95:
            k = randrange(len(free_spaces))
            i,j = free_spaces[k]
            board[i][j] = LIFE
            free_spaces = free_spaces[:k] + free_spaces[k+1:]

# For Testing
b = Board(1)
