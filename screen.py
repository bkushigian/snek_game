from sys import exit
import time
from externs import *

try:
    import curses
except:
    print "Could not import ncurses. Exiting"
    exit(1)

# Colors for drawing, not initialized
CYAN     =   None
YELLOW   =   None
RED      =   None
WHITE    =   None
GREEN    =   None
MAGENTA  =   None
BLUE     =   None


class ColorScheme(object):
    def __init__(self, style='normal'):
        '''
        Color Pairs:
            1:    Cyan       ?
            2:    Blocks
            3:    Apples
            4:    White      ?
            5:    Snake Body
            6:    Snake Head
            7:    Blue       ?
        '''
        # TODO: Write a nice interface for color pairs

        self.style = style
        curses.start_color()
        self._schemes = {'normal': self.normal, 'inverted': self.inverted,
            'mono':self.mono, 'mono-inverted' : self.mono_inverted}

        self._glyph_to_color_pair = {
            MONEY:      1, 
            BLOCK:      2,
            APPLE:      3,
            SPACE:      4,
            SNAKEBODY:  5,
            HEADLEFT:   6,
            HEADRIGHT:  6,
            HEADUP:     6,
            HEADDOWN:   6,
            LIFE:       7
           } 
        self.set_scheme(self.style)

    def normal(self):
        curses.init_pair(1, curses.COLOR_CYAN,    curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW,  curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED,     curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_WHITE,   curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_GREEN,   curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_BLUE,    curses.COLOR_BLACK)

    def inverted(self):
        # TODO: Test this
        curses.init_pair(1, curses.COLOR_BLACK,   curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_YELLOW,  curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_RED,     curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_WHITE,   curses.COLOR_WHITE)
        curses.init_pair(5, curses.COLOR_GREEN,   curses.COLOR_WHITE)
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
        curses.init_pair(7, curses.COLOR_BLUE,    curses.COLOR_WHITE)

    def mono(self):
        curses.init_pair(1, curses.COLOR_WHITE  , curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE  , curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_WHITE  , curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_WHITE  , curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_WHITE  , curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_WHITE  , curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_WHITE  , curses.COLOR_BLACK)

    def mono_inverted(self):
        curses.init_pair(1, curses.COLOR_BLACK  , curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_BLACK  , curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_BLACK  , curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_BLACK  , curses.COLOR_WHITE)
        curses.init_pair(5, curses.COLOR_BLACK  , curses.COLOR_WHITE)
        curses.init_pair(6, curses.COLOR_BLACK  , curses.COLOR_WHITE)
        curses.init_pair(7, curses.COLOR_BLACK  , curses.COLOR_WHITE)
        

    def color_from_glyph(self, c):
        if c in self._glyph_to_color_pair:
            return curses.color_pair(self._glyph_to_color_pair[c])
        return curses.color_pair(0)  # Bad choice.

    def set_scheme(self, s = 'normal'):
        if s in self._schemes:
            self._schemes[s]()

class Screen(object):
    ''' Screen class, handles ncurses calls
    To initialize, first create a board class b = board.Board(),
    and pass it to this constructor:
        scrn = screen.Screen(b)

    '''
    def __init__(self, board = None, setup = True):
        self.board = board
        self.to_draw = []      # Buffer of drawables
        self.dims = (-1, -1)
        self.top_left = (4,2)

        # The following should really be a list (or even a tuple)
        self._head_char = {UP:HEADUP, DOWN:HEADDOWN, LEFT:HEADLEFT, RIGHT:HEADRIGHT}
        if setup:
            self.setup()

    def setup(self):
        ''' Basic ncurses setup'''
        global CYAN, YELLOW, RED, WHITE, GREEN, MAGENTA, BLUE
        self.screen = curses.initscr()
        self.colorscheme = ColorScheme()
        # Get dimensions
        self.dims = self.screen.getmaxyx()

        # Other options
        self.screen.nodelay(1)
        curses.noecho()
        curses.cbreak()
        # TODO: Something about cbreak?

    def draw_board(self):
        ''' Draw board '''
        self.dims = self.screen.getmaxyx()
        if self.dims[0] + 8 < BOARD_HEIGHT or self.dims[1] + 5 < BOARD_WIDTH:
            self.teardown()
            raise RuntimeError("Screen is too small. Please resize")

        self.top_left = (6, self.dims[1] / 2 - (BOARD_WIDTH / 2))
        # FIXME: Make efficient. Keep track of changes. Currently redraws the
        # ENTIRE BOARD, one char at a time. This is dumb and shouldn't happen.
        # So fix this.

        board = self.board
        
        # FIRST: Draw Score
        # TODO

        # THEN: Draw Board
        for y in range(len(board.board)):
            for x in range(len(board.board[y])):
                self.write_board_char(y,x)
        
        # THEN: Draw Snake
        for (y,x) in board.snake[:-1]:
            self.write_board_char(y, x, SNAKEBODY)
        y,x = board.snake[-1]
        HEADCHAR = self._head_char[board.current_direction]
        self.write_board_char(y, x, HEADCHAR)
        self.screen.move(0,0)
        self.screen.refresh()

    def write_board_char(self, y,x, char = None):
        transy = y + self.top_left[0]
        transx = x + self.top_left[1]

        if transy < 0 or transy >= self.dims[0]:
            self.teardown()
            raise RuntimeError(
                "Screen height is too small: y = {} >= {} Please resize".format(
                    transy, self.dims[0]))

        if transx < 0 or transx >= self.dims[1]:
            self.teardown()
            raise RuntimeError(
                "Screen width it too narrow: x = {} >= {} Please resize".format(
                    transx, self.dims[1]))

        if char == None:
            c = self.board.board[y][x]
        else:
            c = char
        if c in (SECRET, SECRETLIFE):
            c = BLOCK
        self.screen.addstr(transy, transx, c, self.colorscheme.color_from_glyph(c))

    def write_to_screen(self, s, y = 0, x = 0, sleep = 1):
        self.dims = self.screen.getmaxyx()
        dims = self.dims
        screen = self.screen
        screen.clear()
        screen.addstr(y, x, s)
        screen.move(dims[0] - 1, dims[1]-1)
        screen.refresh()

    def teardown(self):
        curses.echo(); self.screen.keypad(0); curses.nocbreak();
        curses.endwin()

    def test_write(self):
        ''' Test writing to the screen '''
        self.write_to_screen(s = "Hello World")
        time.sleep(1)
        self.clear()
        self.teardown()

    def clear(self):
        self.screen.clear()

    def set_scheme(self, scheme = 'normal'):
        self.colorscheme.set_scheme(scheme)

    def centered_string_x(self, string):
        ''' Get the starting coordinate of a centered string '''
        return (self.getmaxyx()[1]/2 - len(string)/2)

    # The following are wrappers for curses functions
    def getch(self):
        return self.screen.getch()

    def getmaxyx(self):
        return self.screen.getmaxyx()

    def addstr(self, *args):
        self.screen.addstr(*args)

    def refresh(self):
        self.screen.refresh()

    def clear(self):
        self.screen.clear()

