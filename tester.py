import traceback

from externs import *
import board
import audio
import menu
import screen
import time
from action import *
from game import Game

global_audio = None
exceptions = []

def main():
    try:
        '''
        test_audio()
        test_action()
        test_screen()
        test_board()
        '''
        test_game()
        print "SUCCESS"
    except Exception as e:
        print e
        traceback.print_exc()
        exceptions.append(e)

    for e in exceptions:
        print e

    if global_audio != None:
        global_audio.music.fadeout(4000)
        time.sleep(4.2)

 
def test_action():
    try:
        b = board.Board(1)
        apple_action = EatAppleAction(b, global_audio.chomp.play)

        apple_action.perform(3,2)
        time.sleep(1)
        apple_action.perform(3,2)
        time.sleep(1)
    except Exception as e:
        print e
        exceptions.append(e)
        traceback.print_exc()

def test_audio():
    global global_audio
    try:
        a = audio.Audio()

        a.play_audio('chomp')
        time.sleep(.2)

        a.play_audio('money')
        time.sleep(.2)

        a.play_audio('life')
        time.sleep(.2)

        a.play_audio('block')
        time.sleep(.2)

        a.play_audio('gameOver')
        time.sleep(.2)

        a.play_audio('levelWin')
        time.sleep(1.5)
        a.play_music()
        time.sleep(1.5)
        a.fadeout_music(3000)
        time.sleep(3.0)
        a.add_music('Wanks1.wav')
        a.play_music()
        time.sleep(1)
        global_audio = a
    
    except Exception as e:
        print e
        exceptions.append(e)
        traceback.print_exc()

def test_screen():
    try:
        b   = board.Board(1)
        scr = screen.Screen(b)
        scr.draw_board()

        time.sleep(.1)
        scr.set_scheme('inverted')
        scr.draw_board()
        time.sleep(.1)
        scr.set_scheme('mono')
        scr.draw_board()
        time.sleep(.1)
        scr.set_scheme('mono-inverted')
        scr.draw_board()
        time.sleep(.1)
        scr.set_scheme('normal')
        scr.draw_board()
        scr.teardown()
        return True

    except Exception as e:
        print e
        exceptions.append(e)
        traceback.print_exc()
        return False

def test_board():
    b = board.Board(1)
    scr = screen.Screen(b)
    b.set_screen(scr)
    try:
        for i in range(20):
            b.draw()
            b.move(RIGHT)
            time.sleep(.2)

        for i in range(20):
            b.draw()
            b.move(DOWN)
            time.sleep(.2)

        for i in range(20):
            b.draw()
            b.move(RIGHT)
            time.sleep(.2)

        scr.teardown()
    except Exception as e:
        scr.teardown()
        print e
        exceptions.append(e)
        traceback.print_exc()

def test_game():
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
        exceptions.append(e)
        traceback.print_exc()


if __name__ == '__main__':
    main()
