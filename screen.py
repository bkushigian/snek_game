from sys import exit

dims = screen.getmaxyx() #should return tuple AT LEAST 30x80

try:
    import curses
except:
    print "Could not import ncurses. Exiting"
    exit(1)

class Screen(object):
    def __init__(self, board):
        self.board = board
        difficulty = selectDifficulty()
        self.setup()

    def setup(self):
        ''' Basic ncurses setup'''
        self.screen = curses.initscr()
        # Color options
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_BLUE, curses.COLOR_BLACK)

        # Other options
        self.screen.nodelay(1)
        curses.noecho()

    def draw(self):
        ''' Draw board '''
        pass 

    def write_screen(self, s, y = 0, x = 0, sleep = 1):
        screen = self.screen

        screen.clear()
        screen.addstr(y, x, s)
        screen.move(dims[0] - 1, dims[1]-1)
        screen.refresh()
        time.sleep(sleep)

    def teardown(self):
        curses.endwin()
