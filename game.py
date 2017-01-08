import os
from action   import *
from audio    import Audio
from board    import Board
from externs  import *
from screen   import Screen
from menu     import Menu
import time

class Game(object):
    ''' 
    The Game class handles the meta logic of the game. It is responsible for the
    main while loop on that runs WyRm
    '''
    def __init__(self, screen = None,  level = 1, score = 0):
        self.audio = Audio()   # Runs sounds/music
        self.level = level
        self.score = score

        if screen:
            self.screen = screen
        else:
            self.screen = Screen(setup = False) # Don't go into curses mode yet

        # Board on which we will be playing
        self.board = Board(screen = self.screen, level = self.level, score = self.score, game = self)

        self.menus   = {}  # Map strings like 'main-menu' to menu objects
        self.config  = {}  # Map strings like 'sleep-time' to config options
        self.actions = {}  # Map strings like 'apple' to actions 

        self.handle = void  # An empty function

        # Hard Coded Presets -- should be handled by config dictionary
        self.sleeptime = 0.17

    def setup(self):
        self.screen.setup()
        board = self.board
        audio = self.audio
        actions = self.actions
        appleAction = EatAppleAction(board, audio.chomp.play)
        moneyAction = EatMoneyAction(board, audio.money.play)
        blockAction = HitBlockAction(board, audio.block.play)
        lifeAction  = EatLifeAction (board, audio.life.play )
        gameOverAction = GameOverAction(board, self.screen, audio.gameover.play)
        levelWinAction = LevelWinAction(board, self.screen, audio.levelwin.play)
        
        actions['apple']    = appleAction.perform
        actions['money']    = moneyAction.perform
        actions['block']    = blockAction.perform
        actions['life' ]    = lifeAction.perform
        actions['gameover'] = gameOverAction.perform
        actions['levelwin'] = levelWinAction.perform

        board.set_actions(actions)
        audio.music.queue(os.path.join(MEDIA,'music.wav'))
        audio.music.play()

    def teardown(self):
        self.audio.music.fadeout(1200)
        time.sleep(1)
        self.screen.teardown()

    def run_current_level(self):
        ''' Run the current level on the board '''
        screen      = self.screen
        board       = self.board
        sleeptime   = self.sleeptime
        handle      = board.handle

        # Load the current level
        board.load_level(self.level)

        apples = board.number_of_apples
        for line in board.board:
            for c in line:
                if c == '@':
                    apples += 1
        # MAIN LOOP
        while apples > 0:
            board.set_screen(screen)
            c = ' '
            c = screen.getch()
            screen.addstr(0,0,str(c))
            board.handle(c)
            move_result = board.move()
            board.draw()
            if move_result == WE_HAVE_DIED:
                # Handle life loss, do we lose game?
                board.lives -= 1
                if board.lives <= 0:
                    return WE_HAVE_DIED
                else:
                    board.init_snake()
            if move_result == WE_HAVE_WON:
                return WE_HAVE_WON
            
            time.sleep(sleeptime)

    def load_next_level(self):
        ''' Go to the next level (usually called after a level is won) '''
        self.level += 1
        

    def load_level(self, level):
        ''' Look up and load a level '''
        pass

    def run(self):
        pass

    def pause(self):
        getch = self.screen.getch
        while getch() == -1:
            continue

    def set_current_level(self, level):
        pass

