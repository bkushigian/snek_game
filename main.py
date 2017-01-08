import time
import random
from sys import exit
from os import path

# Local Imports

from audio import Audio
from board import Board
from screen import Screen
from externs import *
from game import Game


def main():
    ''' Main function. Creates board, screen, etc. '''
    game = Game()
    try:
        game.setup()
        while True:
            result = game.run_current_level()
            if result == WE_HAVE_DIED:
                break
            elif result == WE_HAVE_WON:
                game.load_next_level()
            else:
                raise RuntimeError("Shouldn't reach this state")

        game.teardown()
    except Exception as e:
        game.teardown()
        print e

if __name__ == '__main__':
    main()
