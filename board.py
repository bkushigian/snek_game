class Board(object):
    def __init__(self, level):
        pass
        
    def pause(self):
        screen.clear()
        screen.addstr(dims[0]/2, dims[1]/2 - 6, 'GAME PAUSED')
        screen.move(dims[0]-1, dims[1]-1)
        screen.refresh()
        screen.nodelay(0)
        screen.getch()
        screen.nodelay(1)
        screen.clear()
        writeScoreBoard()
        writeEnemies(enemyList)

        writeApples(appleList)

        writeMoney(moneyList)

        writeHiddenSpaces(hiddenSpaceList, cEGGS)

        screen.move(dims[0]-1, dims[1]-1)  
        screen.refresh()
        time.sleep(.2)
  
