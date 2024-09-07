import time
from sys import exit, argv
from os import path

# Local Imports

from audio import Audio
from board import Board
from screen import Screen
from externs import *
from game import Game
import traceback


def main():
    ''' Main function. Creates board, screen, etc. '''
    if len(argv) > 1:
        if argv[1] == 'random':
            try:
                input("Playing Random Mode!!! [Hit any key to continue]")
                game = Game()
                game.setup()
                result = game.run_random_level()
                if result == WE_HAVE_DIED:
                    pass
                elif result == WE_HAVE_WON:
                    raise RuntimeError("Random mode should never be won")
                else:
                    raise RuntimeError("Shouldn't reach this state")

            except Exception as e:
                game.teardown()
                raise e
        return

    try:
        game = Game()
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
        raise e

if __name__ == '__main__':
    main()
