from os import path
from sys import exit

BOARD_HEIGHT = 35
MAXLEVEL     = 16

BLOCK        = '#'
SPACE        = ' '
APPLE        = '@'
MONEY        = '$'
LIFE         = '+'
SECRET       = 'S'
XTRA         = 'x'
SECRET_XTRA  = 'x'

class Board(object):
    def __init__(self, level, screen = None):

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

        self.board = [list(line) for line in lines[:BOARD_HEIGHT]]

        for line in lines[BOARD_HEIGHT:]:
            if line.startswith('name'):
                self.name = line.split('=')[1]
            elif line.startswith('sleep'):
                self.sleepTime = float(line.split('=')[1])
            elif line.startswith('appt'):
                self.applePoints = int(line.split('=')[1])
            elif line.startswith('mnpt'):
                self.moneyPoints = int(line.split('=')[1])
            elif line.startswith('text'):
                self.hint = line.split('=')[1]
            else:
                break
        
