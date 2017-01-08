'''Some system wide variables to be used'''

SCOREBOARD_HEIGHT = 6
BOARD_HEIGHT = 35
BOARD_WIDTH  = 80 # XXX: Is this right?
MAXLEVEL     = 16

BLOCK        = '#'
SPACE        = ' '
SNAKEBODY    = '*'
HEADLEFT     = '<'
HEADRIGHT    = '>'
HEADUP       = '^'
HEADDOWN     = 'v'
APPLE        = '@'
MONEY        = '$'
LIFE         = '+'
SECRET       = 'S'
SECRETLIFE   = 'X'

LEFT, DOWN, UP, RIGHT = 0, 1, 2, 3
WE_HAVE_DIED    = 0
WE_HAVE_WON     = 1
WE_KEEP_PLAYING = 2

MEDIA = 'media'
def void(*args):
    return
