'''
The Handler class handles character input, obtained from curses.getch(). This
currently only has the single method `handle(ch)` that handles an input char.
'''
class Handler(object):
    '''A basic class to handle character input'''
    def __init__(self):
        pass

    def handle(self, ch):
        ''' The null handler '''
        return
