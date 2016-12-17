"""Current Dev: use delchar instead of rewriting everything.

  CURRENT DEV:  
  Implement menu"""

import curses
import time
import random
from sys import exit
from os import path

importSuccess = True
try:  
  import pygame
  import pygame.mixer

except ImportError:
  print "Couldn't import pygame"
  importSuccess = False

####

MEDIA = 'media'
if importSuccess:
  pygame.init()
  pygame.mixer.init()
  pygame.mixer.music.load(path.join(MEDIA, 'music.wav'))
  chomp = pygame.mixer.Sound(path.join(MEDIA, 'chomp.wav'))
  chomp.set_volume(.8)
  money = pygame.mixer.Sound(path.join(MEDIA, 'money.wav'))
  life = pygame.mixer.Sound(path.join(MEDIA,'life.wav'))
  block = pygame.mixer.Sound(path.join(MEDIA, 'block.wav'))
  gameover = pygame.mixer.Sound(path.join(MEDIA,'gameOver.wav'))
  levelwin = pygame.mixer.Sound(path.join(MEDIA,'levelwin.wav'))

else:
    print "Exiting"
    exit(1)

###myList holds [y, x] values

soundList       = [chomp, money, life, block, gameover, levelwin]
myList          = [[2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6]]
appleList       = []
enemyList       = []
moneyList       = []
movingEnemyList = []
xtraLifeList    = []
hiddenSpaceList = []

######MOVING ENEMIES TEMPLATE######

# [y, x, starttime, updatetime, [rightturn],[upturn], [leftturn], [downturn]]
# can also accept form:
# [y, x, starttime, updatetime]

repeat = True; points = 0; sleepTime = .2; 
currentLevel = 0
direction = 1 # 0: UP, 1: RIGHT, 2: DOWN, 3: LEFT
UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3
apMOD = 1; mpMOD = 1; applePoints = 5; moneyPoints = 25
cheat = False; headChar = '>'; difficulty = 1
gameTime = 0; lives = 3; mortal = True; cEGGS = False


##### MENU #####
def menu():
  currentPos = 0
  string1 = "AUDIO"
  string2 = "DIFFICULTY"
  string4 = "EXIT"
  string3 = "RETURN TO GAME"

  q = -1
  repeat = True
  while repeat == True:
    colorList = [curses.color_pair(1),curses.color_pair(1),curses.color_pair(1),curses.color_pair(1)]
    
    colorList[currentPos] = curses.color_pair(2)
    
    screen.clear()
    screen.addstr(dims[0] / 2 - 6, (dims[1] - len(string1)) / 2, string1, colorList[0])
    screen.addstr(dims[0] / 2 - 2, (dims[1] - len(string2)) / 2, string2, colorList[1])
    screen.addstr(dims[0] / 2 + 2, (dims[1] - len(string3)) / 2, string3, colorList[2])
    screen.addstr(dims[0] / 2 + 6, (dims[1] - len(string4)) / 2, string4, colorList[3])
    screen.move(dims[0] - 1, dims[1] - 1)
    screen.refresh()
    q = screen.getch()
    if q == ord('x'):
      repeat = False

    if q == ord('w'):
      currentPos += 3
      currentPos %= 4
    elif q == ord('s'):
      currentPos += 1
      currentPos %= 4
    elif q == 10:
      if currentPos == 0:
        audio()
      elif currentPos == 1:
#         global difficulty
#         difficulty = updateDifficulty()
        pass #DIFFICULTY
      elif currentPos == 2: #RETURN TO GAME
        
        screen.clear()
        writeEnemies(enemyList)
        writeApples(appleList)
        writeMoney(moneyList)
        writeXtraLife(xtraLifeList)
        writeHiddenSpaces(hiddenSpaceList, cEGGS)
        screen.move(dims[0] - 1, dims[1] - 1)
        screen.refresh()
        return False 
      elif currentPos == 3: # EXIT
        
        pygame.mixer.music.fadeout(500)    
        GAMEOVER = 'GAME OVER'
        gameover.play()
        for i in range(len(GAMEOVER)):
          for j in range(dims[0]/2):
            screen.clear()
      
            for k in range(i):
              screen.addstr(dims[0]/2, dims[1]/2 - 8 + 2*k, GAMEOVER[k])
            screen.addstr(j, dims[1]/2 - 8 + 2*i, GAMEOVER[i])
            screen.move(dims[0]-1, dims[1]-1)
            screen.refresh()
            time.sleep(.03)
        screen.clear()
        for i in range(len(GAMEOVER)):
          screen.addstr(dims[0]/2, dims[1]/2 - 8 + 2*i, GAMEOVER[i])    
        screen.move(dims[0]-1, dims[1]-1)
        screen.refresh()
        time.sleep(1.5)
        return True
# def difficulty():
#   global difficulty
#   while 1:
#   screen.clear()
#   screen.addstr(dims[0] / 2, dims[1] / 2 - 5, 'DIFFICULTY', curses.color_pair(1)
#   screen.addstr(dims[0] / 2 + 1, dims[1] / 2 - 1, '%d' % (difficulty), curses.color_pair(2)
#   q = screen.getch()
#   if q == ord('w') or q == ord('d'):
#     difficulty += 1
#   return difficulty
      
def audio():
  currentPos = 0

  string1 = "MUSIC VOLUME"
  string2 = "SOUND FX VOLUME"
  string3 = "MAKE A RANDOM NOISE"
  string4 = "MAIN MENU"
  
  global soundList
  musicVol = pygame.mixer.music.get_volume()
  soundVol = pygame.mixer.Sound.get_volume(soundList[0])
       
  while 1:
    colorList = [curses.color_pair(1),curses.color_pair(1),curses.color_pair(1),curses.color_pair(1), curses.color_pair(1)] 
    colorList[currentPos] = curses.color_pair(2)    
    screen.clear()
    
    # AUDIO
    screen.addstr(dims[0] / 2 - 6, (dims[1] - len(string1)) / 2, string1, colorList[0])
    screen.addstr(dims[0] / 2 - 5, dims[1] / 2 - 1, '%d' % (int(musicVol * 10)), curses.color_pair(1))
    
    screen.addstr(dims[0] / 2 - 2, (dims[1] - len(string2)) / 2, string2, colorList[1])
    screen.addstr(dims[0] / 2 - 1, dims[1] / 2 - 1, '%d' % (int(soundVol * 10)), curses.color_pair(1))
    
    screen.addstr(dims[0] / 2 + 2, (dims[1] - len(string3)) / 2, string3, colorList[2]) 
    screen.addstr(dims[0] / 2 + 6, (dims[1] - len(string4)) / 2, string4, colorList[3])
    screen.move(dims[0] - 1, dims[1] - 1)
    screen.refresh()
    q = screen.getch()
    
    if q == ord('w'):
      currentPos += 3
      currentPos %= 4
    elif q == ord('s'):
      currentPos += 1
      currentPos %= 4
    elif q == 10:
      if currentPos == 0:
        musicVol = musicVolume(musicVol)
        #MUSIC VOLUME
      elif currentPos == 1:
        pass
        soundVol, soundList = fxVolume(soundVol, soundList)
        #SOUND FX VOLUME
      elif currentPos == 2:
        pass
        num = random.choice(range(6))
        soundList[num].play()
        for i in soundList:
          i.set_volume(soundVol)
        #MAKE A RANDOM NOISE
      elif currentPos == 3:
        #MAIN MENU
        return

def fxVolume(soundVol, soundList):
  while 1:
    screen.addstr(dims[0] / 2 - 1, dims[1] / 2 - 1, '%d ' % (int(soundVol * 10)), curses.color_pair(2))
    screen.move(dims[0]-1, dims[1] - 1)
    screen.refresh()
    q = screen.getch()
    if q == ord('w') or q == ord('d'):
      soundVol += .1
      if soundVol > 1.0:
        soundVol = 1.0
      soundList[0].set_volume(soundVol)
      soundList[0].play()
    elif q == ord('s') or q == ord('a'):
      soundVol -= .1
      if soundVol < 0.0:
        soundVol = 0.0
      soundList[0].set_volume(soundVol)
      soundList[0].play()
    elif q == 10:
      for i in soundList:
        i.set_volume(soundVol)
      return soundVol, soundList

def musicVolume(musicVol):
  pass
  while 1:
    screen.addstr(dims[0] / 2 - 5, dims[1] / 2 - 1, '%d ' % (int(musicVol * 10)), curses.color_pair(2))
    screen.move(dims[0]-1, dims[1] - 1)
    screen.refresh()
    q = screen.getch()
    if q == ord('w') or q == ord('d'):
      musicVol += .1
      if musicVol > 1.0:
        musicVol = 1.0
      pygame.mixer.music.set_volume(musicVol)
    elif q == ord('s') or q == ord('a'):
      musicVol -= .1
      if musicVol < 0.0:
        musicVol = 0.0
      pygame.mixer.music.set_volume(musicVol)
    elif q == 10:
      return musicVol
      
##### END MENU#####




def takeCode(points, applePoints, moneyPoints, level, mortal, lives, mpMOD, apMOD):
  temp = 0
  cEGGS = False
  while temp < 1:
  
    CODE = raw_input('Enter Code: ')
    if CODE == 'BBDD':
      points += 99999999
      cheat = True
    elif CODE == 'BLCK': #LEVEL 2
      level = 1
      cheat = True
    elif CODE == 'SNAT': #LEVEL 3
      level = 2
      cheat = True
    elif CODE == 'XVXV': #LEVEL 4
      level = 3
      cheat = True   
    elif CODE == 'SSSS': # LEVEL 5
      level = 4
      cheat = True    
    elif CODE == 'PEWW': # LEVEL 6
      level = 5
      cheat = True
    elif CODE == 'SHOT': # LEVEL 7
      level = 6
      cheat = True
    elif CODE == 'JLIA': # LEVEL 8
      level = 7
      cheat = True
    elif CODE == 'MNBS': # LEVEL 9
      level = 8
      cheat = True
    elif CODE == 'MAZE': # LEVEL 10
      level = 9
      cheat = True
    elif CODE == 'SCRT': # LEVEL 11
      level = 10
      cheat = True
    elif CODE == 'SKLL': # LEVEL 12
      level = 11
      cheat = True
       
    elif CODE == 'MNEY': # 100x MONEY MULT
      mpMOD *= 100
      cheat = True    
    
    elif CODE == 'ELPA': # 100x APPLE MULT
      apMOD *= 100
      cheat = True
    
    elif CODE == 'EFIL': # START WITH 999 LIVES
      lives = 999
      
    elif CODE == 'IAMINVINCIBLE': # CANNOT DIE
      mortal = False
    elif CODE == 'PLEASESIRMAYIHAVEANOTHER': # 3 EXTRA WISHES
      temp -= 3
    elif CODE == 'XRAY': # NOT FUNCTIONAL
      cEGGS = True
    else:
      temp = 1
    temp += 1

  return points, applePoints, moneyPoints, level, mortal, lives, mpMOD, apMOD, cEGGS



def writeSnake(myList):
  for i in range(len(myList) - 1):
    screen.addstr(myList[i][0], myList[i][1], '~', curses.color_pair(5))
    screen.addstr(myList[5][0], myList[5][1], headChar, curses.color_pair(6))
  return myList
  
    

def updateSnake(dir):
  repeat = True
  screen.addstr(myList[0][0], myList[0][1], ' ')
  for i in range(5):
    myList[i][0] = myList[i+1][0]
    myList[i][1] = myList[i+1][1]
  if dir == 0: ###UP
    headChar = '^'
    myList[5][0] -= 1
  elif dir == 1:   ###RIGHT
    headChar = '>'
    myList[5][1] += 1      
  elif dir == 2:  ###DOWN
    headChar = 'v'
    myList[5][0] += 1
  elif dir == 3: ###LEFT
    headChar = '<'
    myList[5][1] -= 1
  if myList[5][0] < 0:
    myList[5][0] = 35
  elif myList[5][0] > 35:
    myList[5][0] = 0
  elif myList[5][1] < 0:
    myList[5][1] = 79
  elif myList[5][1] > 79:
    myList[5][1] = 0
  screen.addstr(myList[0][0], myList[0][1], ' ')
  for i in range(len(myList)):
    screen.addstr(myList[i][0], myList[i][1], '~', curses.color_pair(5))
  screen.addstr(myList[5][0], myList[5][1], headChar, curses.color_pair(6))
  return True, headChar

# def menu()
#   string1 = "AUDIO"
#   string2 = "DIFFICULTY"
  
  
  
def unpackText(f):
  name = 'LEVEL'
  enemyList = []
  appleList = []
  moneyList = []
  xtraLifeList = []
  hint = 'Default'
  applePoints = 0
  moneyPoints = 0
  sleepTime = .3
  j = 0
  while 1:
    j += 1
    myString = f.readline()
    if myString[0] == 'V':
      break
    for i in range(len(myString)):
      if myString[i] == '#':
        enemyList.append([j, i])
      elif myString[i] == '@':
        appleList.append([j, i])
      elif myString[i] == '$':
        moneyList.append([j, i])
      elif myString[i] == '+':
        xtraLifeList.append([j, i])
      elif myString[i] == 'S': #HIDDEN SPACE
        hiddenSpaceList.append([j, i])
  while 1:
    myString = f.readline()
    myString = myString.split('=')
    if myString[0] == 'name':
      name = myString[1]
    elif myString[0] == 'sleep':
      sleepTime = float(myString[1])
    elif myString[0] == 'appt':
      applePoints = int(myString[1])
    elif myString[0] == 'mnpt':
      moneyPoints = int(myString[1])
    elif myString[0] == 'text':
      hint = myString[1]
    elif myString[0] == 'mven':
      
      myString = myString[2].split('|')
      for i in myString:
        temp = i.split[',']
        movingEnemyList.append(temp)
    elif myString[0] == '':
      break
    else:
      break
    
  return name, appleList, moneyList, enemyList, xtraLifeList, hiddenSpaceList, hint, applePoints, moneyPoints, sleepTime
  
  
def levelSelect(level):
  repeat = True
  level += 1
  myCode = ' '
  appleList = moneyList = enemyList = hiddenSpaceList = []
  name = hint = ' '
  applePoints = moneyPoint = 0
  sleepTime = .25
  extraList = [] #HOLDS EASTEREGGS MONEY
  extraList2 = [] # HOLDS HIDDEN LIVES
  screen.clear()
  if level != 1:
    screen.addstr(dims[0]/2, dims[1]/2 - 6, 'LEVEL WON!!!', curses.color_pair(4))
    screen.addstr(0, dims[1] / 2 - 14, 'LEVEL: %d          SCORE: %d' % (level, points), curses.color_pair(4))
    screen.refresh()
  if level in range(1, 13):
    f = open(path.join('data','lv{}.txt'.format(level)), 'r')

  if level == 1:
    extraList2.append([35, 79])

  elif level == 2:
    extraList.append([11, 51])
    extraList2 = [[21,26], [3, 0]]

  elif level == 3:
    extraList2.append([16, 66])
    extraList.append([26, 39])

  elif level == 4:
    extraList = [[3,2], [30, 52], [30, 27]]
    extraList2 = [[35, 20]]

  elif level == 5:
    extraList2 = [[33,63], [34, 78]]

  elif level == 6:
    pass
    
  elif level == 7:
    extraList2 = [[19, 12]]

  elif level in (8,9,10,11,12):
    pass
  else:
    winGame()
    repeat = False
    return 0, [], [], [], [], [], '', 0, False
  
  name, appleList, moneyList, enemyList, xtraLifeList, hiddenSpaceList, hint, applePoints, moneyPoints, sleepTime = unpackText(f)

  time.sleep(2)

  for i in extraList:
    moneyList.append(i)
  for i in extraList2:
    xtraLifeList.append(i)
  
###UPDATE SCREEN###

  screen.clear()
  screen.addstr(dims[0]/2 - 2, dims[1]/2 - 4, 'LEVEL %d' % level)
  screen.addstr(dims[0]/2, dims[1]/2 - len(name) / 2, name)
  screen.addstr(dims[0]/2 + 2, dims[1]/2 - len(hint) / 2, hint)    
  screen.move(dims[0]-1, dims[1]-1)     
  screen.refresh()
  time.sleep(1.5)    
  
  screen.clear()
  writeEnemies(enemyList)
  
  writeApples(appleList)
  
  writeMoney(moneyList)
  
  writeXtraLife(xtraLifeList)
  writeHiddenSpaces(hiddenSpaceList, cEGGS)
             
  return level, appleList, enemyList, moneyList, xtraLifeList, hiddenSpaceList, hint, sleepTime, repeat   

def pause():
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
  

def writeScoreBoard():
  screen.addstr(0, dims[1] / 2 - 27, 'LEVEL: %d          SCORE: %d            LIVES: %d' % (currentLevel, points, lives), curses.color_pair(4))      
  screen.move(dims[0]-1, dims[1]-1)


def gameOver(enemyList, appleList, moneyList, myList, xtraLifeList, hiddenSpaceList, level, lives):
  lives -= 1
  if lives > 0:
    for i in range(4):

      for i in range(len(myList) - 1): 
        screen.addstr(myList[i][0], myList[i][1], '*', curses.color_pair(5))
      screen.addstr(myList[5][0], myList[5][1], headChar, curses.color_pair(6))
      screen.move(dims[0] - 1, dims[1] - 1)      
      screen.refresh()
      time.sleep(.4)

      for i in myList:
        screen.addstr(i[0], i[1], ' ')
      screen.move(dims[0] - 1, dims[1] - 1)
      screen.refresh()
      time.sleep(.25)
        
    level -= 1
    #levelSelect(level)
    myList = [[2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6]]
    writeEnemies(enemyList)
    direction = 1
    g = screen.getch()
    while g != -1:
      g = screen.getch()
    
    
    return True, lives, myList, direction

  else:  
    for i in range(6):
        for i in range(len(myList) - 1): 
          screen.addstr(myList[i][0], myList[i][1], '*', curses.color_pair(5))
        screen.addstr(myList[5][0], myList[5][1], headChar, curses.color_pair(6))
        screen.move(dims[0] - 1, dims[1] - 1)        
        screen.refresh()
        time.sleep(.4)

        for i in myList:
          screen.addstr(i[0], i[1], ' ')
        screen.move(dims[0] - 1, dims[1] - 1)          
        screen.refresh()
        time.sleep(.25)
    pygame.mixer.music.fadeout(500)    
    GAMEOVER = 'GAME OVER'
    gameover.play()
    for i in range(len(GAMEOVER)):
      for j in range(dims[0]/2):
        screen.clear()
      
        for k in range(i):
          screen.addstr(dims[0]/2, dims[1]/2 - 8 + 2*k, GAMEOVER[k])
        screen.addstr(j, dims[1]/2 - 8 + 2*i, GAMEOVER[i])
        screen.move(dims[0]-1, dims[1]-1)
        screen.refresh()
        time.sleep(.03)
    screen.clear()
    for i in range(len(GAMEOVER)):
      screen.addstr(dims[0]/2, dims[1]/2 - 8 + 2*i, GAMEOVER[i])    
    screen.move(dims[0]-1, dims[1]-1)
    screen.refresh()
    time.sleep(1.5)
    return False, lives, myList, 1

def captureMove(direction):
  q = screen.getch()
  exitGame = False
  if q == ord('w'):
    direction = 0
  elif q == ord('s'):
    direction = 2
  elif q == ord('a'):
    direction = 3
  elif q == ord('d'):
    direction = 1
  elif q == ord('p'):
    pause()
  elif q == ord('m'):
    exitGame = menu()
  return q, direction, exitGame
  
  


  
  
def writeEnemies(enemyList):
  for i in range(len(enemyList)):
    screen.addstr(enemyList[i][0], enemyList[i][1], '#', curses.color_pair(2))
    screen.move(dims[0]-1, dims[1] - 1)

def writeApples(appleList): 
  for i in range(len(appleList)):
    screen.addstr(appleList[i][0], appleList[i][1], '@', curses.color_pair(3))
    screen.move(dims[0]-1, dims[1] - 1)

def writeMoney(moneyList):
  for i in range(len(moneyList)):
    screen.addstr(moneyList[i][0], moneyList[i][1], '$', curses.color_pair(1))
    screen.move(dims[0]-1, dims[1] - 1)

def writeXtraLife(xtraLifeList):
  for i in xtraLifeList:
    screen.addstr(i[0], i[1], '+', curses.color_pair(3))
    screen.move(dims[0]-1, dims[1] - 1)

def writeHiddenSpaces(hiddenSpaceList, cEGGS):
  cEGGS = False
  if cEGGS == False:
    for i in hiddenSpaceList:
      screen.addstr(i[0], i[1], '#', curses.color_pair(2))

  else:
    pass
  screen.move(dims[0]-1, dims[1] - 1)
  screen.refresh()


  
def writeToScreen(myStr, y = 0, x = 0, tempSleepTime = 1):
  screen.clear()
  screen.addstr(y, x, myStr)
  screen.move(dims[0] - 1, dims[1]-1)
  screen.refresh()
  time.sleep(tempSleepTime)
  
def selectDifficulty():
  temp = raw_input('\n\n\n\n\nSELECT DIFFICULTY:\n\n\n\n\n(1) Novice\n(2) Easy\n(3) Normal \n(4) Hard\n(5)INSAAAANE\n\n\n')
  if temp == '1':
    temp = 1.75
  elif temp == '2':
    temp = 1.3  
  elif temp == '4':
    temp = .65
  elif temp == '5':
    temp = .28
  else:
    temp = 1
  return temp


def winGame():
  screen.clear()
  snakeList = [[2,3], [2,4], [2,5], [2,6], [2,7], [2,8]]
  screen.addstr(dims[0] / 2, dims[1] / 2 - 5, 'YOU WON!!!')
  screen.move(dims[0]-1, dims[1]-1)
  screen.refresh
  time.sleep(1)
  
#################START PROGRAM!!!!!!######################
difficulty = selectDifficulty()
points, applePoints, moneyPoints, currentLevel, mortal, lives, mpMOD, apMOD, cEGGS = takeCode(points, applePoints, moneyPoints, currentLevel, mortal, lives, mpMOD, apMOD)

  
screen = curses.initscr()

#########COLORS##########
curses.start_color()
curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
curses.init_pair(7, curses.COLOR_BLUE, curses.COLOR_BLACK)


screen.nodelay(1)
curses.noecho()
dims = screen.getmaxyx() #should return tuple 30x80
q = -1

writeToScreen('BEGIN!!!', dims[0] / 2, dims[1] / 2 - 4, .5)
if importSuccess == True:
  pygame.mixer.music.play(1000)

time.sleep(1)

currentLevel, appleList, enemyList, moneyList, xtraLifeList, hiddenSpaceList, hint, sleepTime, repeat = levelSelect(currentLevel)
repeat = True
while repeat == True:

  gameTime += 1

  time.sleep(sleepTime * difficulty)
  
  writeHiddenSpaces(hiddenSpaceList, cEGGS)
    
  q, direction, exitGame = captureMove(direction)
  if exitGame == True:
    break
  repeat, headChar = updateSnake(direction)  
  
  writeScoreBoard()

  screen.move(dims[0]-1, dims[1]-1) 
  screen.refresh()
  
  gotApple = [False, []]
  for i in appleList:
    if myList[5] == i:
      chomp.play()
      gotApple[0], gotApple[1] = True, i
      points += applePoints*apMOD
  if  gotApple[0] == True:
    del(appleList[appleList.index(gotApple[1])])
   
  gotLife = [False, []] 
  for i in xtraLifeList:
    if myList[5] == i:
      gotLife[0], gotLife[1] = True, i
      lives += 1
      life.play()
      writeScoreBoard()
    if gotLife[0] == True:
      del(xtraLifeList[xtraLifeList.index(gotLife[1])])
      
  if mortal == True:      
    for i in enemyList:
      if myList[5] == i:
        block.play()
        repeat, lives, myList, direction = gameOver(enemyList, appleList, moneyList, myList, xtraLifeList, hiddenSpaceList, currentLevel, lives)
  
  gotMoney = [False, []]
  for i in moneyList:
    if myList[5] == i:
      gotMoney[0], gotMoney[1] = True, i
      money.play()
      points += moneyPoints*mpMOD
  if gotMoney[0] == True:
      del(moneyList[moneyList.index(gotMoney[1])])
  
  if len(appleList) == 0:
    time.sleep(.1)
    hiddenSpaceList = []
    levelwin.play()
    currentLevel, appleList, enemyList, moneyList, xtraLifeList, hiddenSpaceList, hint, sleepTime, repeat = levelSelect(currentLevel)
    time.sleep(2)
    myList = [[2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6]]
    screen.refresh()
    time.sleep(1)
    curses.flushinp()
    direction = 1

    
  ###CHECK MOVING ENEMIES
#   for i in movingEnemyList:
#     for j in myList:
#       if i[0] == j[0] and i[1] == j[1]:
#         repeat, lives = gameOver(enemyList, appleList, moneyList, myList)
    
  
  

  q, direction, exitGame = captureMove(direction)


curses.endwin()
