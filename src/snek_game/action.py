from externs import *

class Action(object):
    ''' 
    This class describes a thing being done, such as an apple being eaten.
    '''
    audio = None
    def __init__(self, board, *toperform):
        self.board     = board
        self.toperform = toperform
        pass
    def perform(self):
        pass

class EatAppleAction(Action):
    def __init__(self, board, *toperform):
        self.board     = board
        self.toperform = toperform

    def perform(self, y, x):
        for f in self.toperform:
            f()
        self.board.board[y][x] = SPACE
        self.board.grow_snake()

class EatMoneyAction(Action):
    def __init__(self, board, *toperform):
        self.board     = board
        self.toperform = toperform

    def perform(self, y, x):
        for f in self.toperform:
            f()
        self.board.board[y][x] = SPACE

class HitBlockAction(Action):
    def __init__(self, board, *toperform):
        self.board     = board
        self.toperform = toperform

    def perform(self, y, x):
        for f in self.toperform:
            f()

class EatLifeAction(Action):
    def __init__(self, board, *toperform):
        self.board     = board
        self.toperform = toperform

    def perform(self, y, x):
        for f in self.toperform:
            f()
        if self.board[y][x] == SECRETLIFE:
            self.board[y][x] = SECRET
        else:
            self.board.board[y][x] = SPACE
        self.board.lives += 1

class GameOverAction(Action):
    # TODO: Animate the final game over scene
    def __init__(self, board, screen, *toperform):
        self.board     = board
        self.screen    = screen
        self.toperform = toperform

    def perform(self, y, x):
        for f in self.toperform:
            f()

class LevelWinAction(Action):
    # TODO: Animate the final game over scene
    def __init__(self, board, screen, *toperform):
        self.board     = board
        self.screen    = screen
        self.toperform = toperform

    def perform(self, y, x):
        for f in self.toperform:
            f()

