import traceback

from externs import *
import board
import audio
import menu
import screen
import time

def main():
    try:
        b   = board.Board(1)
        scr = screen.Screen(b)
        scr.draw_board()

        time.sleep(1)
        scr.set_scheme('inverted')
        scr.draw_board()
        time.sleep(1)
        scr.set_scheme('mono')
        scr.draw_board()
        time.sleep(1)
        scr.set_scheme('mono-inverted')
        scr.draw_board()
        time.sleep(1)
        scr.set_scheme('normal')
        scr.draw_board()
        '''
        time.sleep(.5)
        scr.set_scheme('inverted')
        scr.draw_board()
        time.sleep(.5)
        scr.set_scheme('mono')
        scr.draw_board()
        time.sleep(.5)
        scr.set_scheme('mono-inverted')
        scr.draw_board()
        time.sleep(.5)

        for i in range(20):
            scr.set_scheme('normal')
            scr.draw_board()
            time.sleep(.05)
            scr.set_scheme('inverted')
            scr.draw_board()
            time.sleep(.05)
            scr.set_scheme('mono')
            scr.draw_board()
            time.sleep(.05)
            scr.set_scheme('mono-inverted')
            scr.draw_board()
            time.sleep(.05)
        '''
        scr.teardown()
        print "SUCCESS"
    except Exception as e:
        print e
        print traceback.print_exc()
 
if __name__ == '__main__':
    main()
