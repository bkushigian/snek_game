#!/usr/bin/env python3
import curses
import pkg_resources
import time
import random
from sys import exit
from os import path as osp

import_success = False
try:  
  import pygame
  import pygame.mixer
  import_success = True

except ImportError:
  print("Couldn't import pygame")

####

RESOURCES = pkg_resources.resource_filename("snek_game", "resources")
MEDIA = osp.join(RESOURCES, 'media')
DATA = osp.join(RESOURCES, 'data')
LEVELS= osp.join(RESOURCES, "levels")
if import_success:
  pygame.init()
  pygame.mixer.init()
  pygame.mixer.music.load(osp.join(MEDIA, 'music.wav'))
  chomp = pygame.mixer.Sound(osp.join(MEDIA, 'chomp.wav'))
  chomp.set_volume(.8)
  money = pygame.mixer.Sound(osp.join(MEDIA, 'money.wav'))
  life = pygame.mixer.Sound(osp.join(MEDIA,'life.wav'))
  block = pygame.mixer.Sound(osp.join(MEDIA, 'block.wav'))
  gameover = pygame.mixer.Sound(osp.join(MEDIA,'gameOver.wav'))
  levelwin = pygame.mixer.Sound(osp.join(MEDIA,'levelWin.wav'))

else:
    print("Exiting")
    exit(1)

###my_list holds [y, x] values

sound_list       = [chomp, money, life, block, gameover, levelwin]
my_list          = [[2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6]]
apple_list       = []
enemy_list       = []
money_list       = []
moving_enemy_list = []
extra_life_list    = []
hidden_space_list = []

######MOVING ENEMIES TEMPLATE######

# [y, x, starttime, updatetime, [rightturn],[upturn], [leftturn], [downturn]]
# can also accept form:
# [y, x, starttime, updatetime]

repeat = True; points = 0; sleep_time = .2;
current_level = 0
direction = 1 # 0: UP, 1: RIGHT, 2: DOWN, 3: LEFT
UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3
apMOD = 1; mpMOD = 1; applePoints = 5; moneyPoints = 25
cheat = False; headChar = '>'; difficulty = 1
game_time = 0; lives = 3; mortal = True; cEGGS = False


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
    color_list = [curses.color_pair(1),curses.color_pair(1),curses.color_pair(1),curses.color_pair(1)]

    color_list[currentPos] = curses.color_pair(2)

    screen.clear()
    screen.addstr(dims[0] // 2 - 6, (dims[1] - len(string1)) // 2, string1, color_list[0])
    screen.addstr(dims[0] // 2 - 2, (dims[1] - len(string2)) // 2, string2, color_list[1])
    screen.addstr(dims[0] // 2 + 2, (dims[1] - len(string3)) // 2, string3, color_list[2])
    screen.addstr(dims[0] // 2 + 6, (dims[1] - len(string4)) // 2, string4, color_list[3])
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
        pass #DIFFICULTY
      elif currentPos == 2: #RETURN TO GAME
        
        screen.clear()
        writeEnemies(enemy_list)
        writeApples(apple_list)
        writeMoney(money_list)
        write_extra_life(extra_life_list)
        write_hidden_spaces(hidden_space_list, cEGGS)
        screen.move(dims[0] - 1, dims[1] - 1)
        screen.refresh()
        return False 
      elif currentPos == 3: # EXIT
        
        pygame.mixer.music.fadeout(500)    
        GAMEOVER = 'GAME OVER'
        gameover.play()
        for i in range(len(GAMEOVER)):
          for j in range(dims[0]//2):
            screen.clear()
      
            for k in range(i):
              screen.addstr(dims[0]//2, dims[1]//2 - 8 + 2*k, GAMEOVER[k])
            screen.addstr(j, dims[1]//2 - 8 + 2*i, GAMEOVER[i])
            screen.move(dims[0]-1, dims[1]-1)
            screen.refresh()
            time.sleep(.03)
        screen.clear()
        for i in range(len(GAMEOVER)):
          screen.addstr(dims[0]//2, dims[1]//2 - 8 + 2*i, GAMEOVER[i])
        screen.move(dims[0]-1, dims[1]-1)
        screen.refresh()
        time.sleep(1.5)
        return True
      
def audio():
  currentPos = 0

  string1 = "MUSIC VOLUME"
  string2 = "SOUND FX VOLUME"
  string3 = "MAKE A RANDOM NOISE"
  string4 = "MAIN MENU"
  
  global sound_list
  musicVol = pygame.mixer.music.get_volume()
  soundVol = pygame.mixer.Sound.get_volume(sound_list[0])
       
  while 1:
    color_list = [curses.color_pair(1),curses.color_pair(1),curses.color_pair(1),curses.color_pair(1), curses.color_pair(1)]
    color_list[currentPos] = curses.color_pair(2)
    screen.clear()
    
    # AUDIO
    screen.addstr(dims[0] // 2 - 6, (dims[1] - len(string1)) // 2, string1, color_list[0])
    screen.addstr(dims[0] // 2 - 5, dims[1] // 2 - 1, '%d' % (int(musicVol * 10)), curses.color_pair(1))
    
    screen.addstr(dims[0] // 2 - 2, (dims[1] - len(string2)) // 2, string2, color_list[1])
    screen.addstr(dims[0] // 2 - 1, dims[1] // 2 - 1, '%d' % (int(soundVol * 10)), curses.color_pair(1))
    
    screen.addstr(dims[0] // 2 + 2, (dims[1] - len(string3)) // 2, string3, color_list[2])
    screen.addstr(dims[0] // 2 + 6, (dims[1] - len(string4)) // 2, string4, color_list[3])
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
        soundVol, sound_list = fxVolume(soundVol, sound_list)
        #SOUND FX VOLUME
      elif currentPos == 2:
        pass
        num = random.choice(range(6))
        sound_list[num].play()
        for i in sound_list:
          i.set_volume(soundVol)
        #MAKE A RANDOM NOISE
      elif currentPos == 3:
        #MAIN MENU
        return

def fxVolume(soundVol, sound_list):
  while 1:
    screen.addstr(dims[0] // 2 - 1, dims[1] // 2 - 1, '%d ' % (int(soundVol * 10)), curses.color_pair(2))
    screen.move(dims[0]-1, dims[1] - 1)
    screen.refresh()
    q = screen.getch()
    if q == ord('w') or q == ord('d'):
      soundVol += .1
      if soundVol > 1.0:
        soundVol = 1.0
      sound_list[0].set_volume(soundVol)
      sound_list[0].play()
    elif q == ord('s') or q == ord('a'):
      soundVol -= .1
      if soundVol < 0.0:
        soundVol = 0.0
      sound_list[0].set_volume(soundVol)
      sound_list[0].play()
    elif q == 10:
      for i in sound_list:
        i.set_volume(soundVol)
      return soundVol, sound_list

def musicVolume(musicVol):
  pass
  while 1:
    screen.addstr(dims[0] // 2 - 5, dims[1] // 2 - 1, '%d ' % (int(musicVol * 10)), curses.color_pair(2))
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
  
    CODE = input('Enter Code: ')
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
    elif CODE == 'JULIA': # LEVEL 8
      level = 7
      cheat = True
    elif CODE == 'BENOIT': # LEVEL 9
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



def writeSnake(my_list):
  for i in range(len(my_list) - 1):
    screen.addstr(my_list[i][0], my_list[i][1], '~', curses.color_pair(5))
    screen.addstr(my_list[5][0], my_list[5][1], headChar, curses.color_pair(6))
  return my_list
  
    

def updateSnake(dir):
  repeat = True
  screen.addstr(my_list[0][0], my_list[0][1], ' ')
  for i in range(5):
    my_list[i][0] = my_list[i+1][0]
    my_list[i][1] = my_list[i+1][1]
  if dir == 0: ###UP
    headChar = '^'
    my_list[5][0] -= 1
  elif dir == 1:   ###RIGHT
    headChar = '>'
    my_list[5][1] += 1
  elif dir == 2:  ###DOWN
    headChar = 'v'
    my_list[5][0] += 1
  elif dir == 3: ###LEFT
    headChar = '<'
    my_list[5][1] -= 1
  if my_list[5][0] < 0:
    my_list[5][0] = 35
  elif my_list[5][0] > 35:
    my_list[5][0] = 0
  elif my_list[5][1] < 0:
    my_list[5][1] = 79
  elif my_list[5][1] > 79:
    my_list[5][1] = 0
  screen.addstr(my_list[0][0], my_list[0][1], ' ')
  for i in range(len(my_list)):
    screen.addstr(my_list[i][0], my_list[i][1], '~', curses.color_pair(5))
  screen.addstr(my_list[5][0], my_list[5][1], headChar, curses.color_pair(6))
  return True, headChar

# def menu()
#   string1 = "AUDIO"
#   string2 = "DIFFICULTY"
  
  
  
def unpackText(f):
  name = 'LEVEL'
  enemy_list = []
  apple_list = []
  money_list = []
  extra_life_list = []
  hint = 'Default'
  applePoints = 0
  moneyPoints = 0
  sleep_time = .3
  j = 0
  while 1:
    j += 1
    myString = f.readline()
    if myString[0] == 'V':
      break
    for i in range(len(myString)):
      if myString[i] == '#':
        enemy_list.append([j, i])
      elif myString[i] == '@':
        apple_list.append([j, i])
      elif myString[i] == '$':
        money_list.append([j, i])
      elif myString[i] == '+':
        extra_life_list.append([j, i])
      elif myString[i] == 'S': #HIDDEN SPACE
        hidden_space_list.append([j, i])
  while 1:
    myString = f.readline()
    myString = myString.split('=')
    if myString[0] == 'name':
      name = myString[1]
    elif myString[0] == 'sleep':
      sleep_time = float(myString[1])
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
        moving_enemy_list.append(temp)
    elif myString[0] == '':
      break
    else:
      break
    
  return name, apple_list, money_list, enemy_list, extra_life_list, hidden_space_list, hint, applePoints, moneyPoints, sleep_time
  
  
def levelSelect(level):
  repeat = True
  level += 1
  myCode = ' '
  apple_list = money_list = enemy_list = hidden_space_list = []
  name = hint = ' '
  applePoints = moneyPoint = 0
  sleep_time = .25
  extra_list = [] #HOLDS EASTEREGGS MONEY
  extra_list2 = [] # HOLDS HIDDEN LIVES
  screen.clear()
  if level != 1:
    screen.addstr(dims[0]//2, dims[1]//2 - 6, 'LEVEL WON!!!', curses.color_pair(4))
    screen.addstr(0, dims[1] // 2 - 14, 'LEVEL: %d          SCORE: %d' % (level, points), curses.color_pair(4))
    screen.refresh()
  if level in range(1, 13):
    f = open(osp.join(LEVELS,'lv{}.txt'.format(level)), 'r')

  if level == 1:
    extra_list2.append([35, 79])

  elif level == 2:
    extra_list.append([11, 51])
    extra_list2 = [[21,26], [3, 0]]

  elif level == 3:
    extra_list2.append([16, 66])
    extra_list.append([26, 39])

  elif level == 4:
    extra_list = [[3,2], [30, 52], [30, 27]]
    extra_list2 = [[35, 20]]

  elif level == 5:
    extra_list2 = [[33,63], [34, 78]]

  elif level == 6:
    pass
    
  elif level == 7:
    extra_list2 = [[19, 12]]

  elif level in (8,9,10,11,12):
    pass
  else:
    winGame()
    repeat = False
    return 0, [], [], [], [], [], '', 0, False
  
  name, apple_list, money_list, enemy_list, xtra_life_list, hidden_space_list, hint, applePoints, moneyPoints, sleep_time = unpackText(f)

  time.sleep(2)

  for i in extra_list:
    money_list.append(i)
  for i in extra_list2:
    xtra_life_list.append(i)
  
###UPDATE SCREEN###

  screen.clear()
  screen.addstr(dims[0]//2 - 2, dims[1]//2 - 4, 'LEVEL %d' % level)
  screen.addstr(dims[0]//2, dims[1]//2 - len(name) // 2, name)
  screen.addstr(dims[0]//2 + 2, dims[1]//2 - len(hint) // 2, hint)
  screen.move(dims[0]-1, dims[1]-1)     
  screen.refresh()
  time.sleep(1.5)    
  
  screen.clear()
  writeEnemies(enemy_list)
  
  writeApples(apple_list)
  
  writeMoney(money_list)
  
  write_extra_life(xtra_life_list)
  write_hidden_spaces(hidden_space_list, cEGGS)
             
  return level, apple_list, enemy_list, money_list, xtra_life_list, hidden_space_list, hint, sleep_time, repeat

def pause():
  screen.clear()
  screen.addstr(dims[0]//2, dims[1]//2 - 6, 'GAME PAUSED')
  screen.move(dims[0]-1, dims[1]-1)
  screen.refresh()
  screen.nodelay(0)
  screen.getch()
  screen.nodelay(1)
  screen.clear()
  writeScoreBoard()
  writeEnemies(enemy_list)
  
  writeApples(apple_list)
  
  writeMoney(money_list)
  
  write_hidden_spaces(hidden_space_list, cEGGS)
  
  screen.move(dims[0]-1, dims[1]-1)  
  screen.refresh()
  time.sleep(.2)
  

def writeScoreBoard():
  screen.addstr(0, dims[1] // 2 - 27, 'LEVEL: %d          SCORE: %d            LIVES: %d' % (current_level, points, lives), curses.color_pair(4))
  screen.move(dims[0]-1, dims[1]-1)


def gameOver(enemy_list, apple_list, money_list, my_list, xtra_life_list, hidden_space_list, level, lives):
  lives -= 1
  if lives > 0:
    for i in range(4):

      for i in range(len(my_list) - 1):
        screen.addstr(my_list[i][0], my_list[i][1], '*', curses.color_pair(5))
      screen.addstr(my_list[5][0], my_list[5][1], headChar, curses.color_pair(6))
      screen.move(dims[0] - 1, dims[1] - 1)      
      screen.refresh()
      time.sleep(.4)

      for i in my_list:
        screen.addstr(i[0], i[1], ' ')
      screen.move(dims[0] - 1, dims[1] - 1)
      screen.refresh()
      time.sleep(.25)
        
    level -= 1
    #levelSelect(level)
    my_list = [[2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6]]
    writeEnemies(enemy_list)
    direction = 1
    g = screen.getch()
    while g != -1:
      g = screen.getch()
    
    
    return True, lives, my_list, direction

  else:  
    for i in range(6):
        for i in range(len(my_list) - 1):
          screen.addstr(my_list[i][0], my_list[i][1], '*', curses.color_pair(5))
        screen.addstr(my_list[5][0], my_list[5][1], headChar, curses.color_pair(6))
        screen.move(dims[0] - 1, dims[1] - 1)        
        screen.refresh()
        time.sleep(.4)

        for i in my_list:
          screen.addstr(i[0], i[1], ' ')
        screen.move(dims[0] - 1, dims[1] - 1)          
        screen.refresh()
        time.sleep(.25)
    pygame.mixer.music.fadeout(500)    
    GAMEOVER = 'GAME OVER'
    gameover.play()
    for i in range(len(GAMEOVER)):
      for j in range(dims[0]//2):
        screen.clear()
      
        for k in range(i):
          screen.addstr(dims[0]//2, dims[1]//2 - 8 + 2*k, GAMEOVER[k])
        screen.addstr(j, dims[1]//2 - 8 + 2*i, GAMEOVER[i])
        screen.move(dims[0]-1, dims[1]-1)
        screen.refresh()
        time.sleep(.03)
    screen.clear()
    for i in range(len(GAMEOVER)):
      screen.addstr(dims[0]//2, dims[1]//2 - 8 + 2*i, GAMEOVER[i])
    screen.move(dims[0]-1, dims[1]-1)
    screen.refresh()
    time.sleep(1.5)
    return False, lives, my_list, 1

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
  
  


  
  
def writeEnemies(enemy_list):
  for i in range(len(enemy_list)):
    screen.addstr(enemy_list[i][0], enemy_list[i][1], '#', curses.color_pair(2))
    screen.move(dims[0]-1, dims[1] - 1)

def writeApples(apple_list):
  for i in range(len(apple_list)):
    screen.addstr(apple_list[i][0], apple_list[i][1], '@', curses.color_pair(3))
    screen.move(dims[0]-1, dims[1] - 1)

def writeMoney(money_list):
  for i in range(len(money_list)):
    screen.addstr(money_list[i][0], money_list[i][1], '$', curses.color_pair(1))
    screen.move(dims[0]-1, dims[1] - 1)

def write_extra_life(extra_life_list):
  for i in extra_life_list:
    screen.addstr(i[0], i[1], '+', curses.color_pair(3))
    screen.move(dims[0]-1, dims[1] - 1)

def write_hidden_spaces(hidden_space_list, cEGGS):
  cEGGS = False
  if cEGGS == False:
    for i in hidden_space_list:
      screen.addstr(i[0], i[1], '#', curses.color_pair(2))

  else:
    pass
  screen.move(dims[0]-1, dims[1] - 1)
  screen.refresh()


  
def writeToScreen(myStr, y = 0, x = 0, tempSleep_time = 1):
  screen.clear()
  screen.addstr(y, x, myStr)
  screen.move(dims[0] - 1, dims[1]-1)
  screen.refresh()
  time.sleep(tempSleep_time)
  
def selectDifficulty():
  temp = input('\n\n\n\n\nSELECT DIFFICULTY:\n\n\n\n\n(1) Novice\n(2) Easy\n(3) Normal \n(4) Hard\n(5)INSAAAANE\n\n\n')
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
  snake_list = [[2,3], [2,4], [2,5], [2,6], [2,7], [2,8]]
  screen.addstr(dims[0] // 2, dims[1] // 2 - 5, 'YOU WON!!!')
  screen.move(dims[0]-1, dims[1]-1)
  screen.refresh
  time.sleep(1)
  
#################START PROGRAM!!!!!!######################
difficulty = selectDifficulty()
points, applePoints, moneyPoints, current_level, mortal, lives, mpMOD, apMOD, cEGGS = takeCode(points, applePoints, moneyPoints, current_level, mortal, lives, mpMOD, apMOD)

  
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

writeToScreen('BEGIN!!!', dims[0] // 2, dims[1] // 2 - 4, .5)
if import_success == True:
  pygame.mixer.music.play(1000)

time.sleep(1)

current_level, apple_list, enemy_list, money_list, extra_life_list, hidden_space_list, hint, sleep_time, repeat = levelSelect(current_level)
repeat = True
while repeat:
  game_time += 1

  time.sleep(sleep_time * difficulty)
  
  write_hidden_spaces(hidden_space_list, cEGGS)
    
  q, direction, exitGame = captureMove(direction)
  if exitGame == True:
    break
  repeat, headChar = updateSnake(direction)  
  
  writeScoreBoard()

  screen.move(dims[0]-1, dims[1]-1) 
  screen.refresh()
  head = my_list[5]
  
  for apple_dims in apple_list:
    if head == apple_dims:
      chomp.play()
      points += applePoints*apMOD
      apple_list.remove(apple_dims)
   
  for extra_life_dims in extra_life_list:
    if head == extra_life_dims:
      lives += 1
      life.play()
      writeScoreBoard()
      extra_life_list.remove(extra_life_dims)
      
  if mortal == True:      
    for enemy_dims in enemy_list:
      if head == enemy_dims:
        block.play()
        repeat, lives, my_list, direction = gameOver(enemy_list, apple_list, money_list, my_list, extra_life_list, hidden_space_list, current_level, lives)
  
  for money_dims in money_list:
    if my_list[5] == money_dims:
      money.play()
      points += moneyPoints*mpMOD
      money_list.remove(money_dims)
  
  if len(apple_list) == 0:
    time.sleep(.1)
    hidden_space_list = []
    levelwin.play()
    current_level, apple_list, enemy_list, money_list, extra_life_list, hidden_space_list, hint, sleep_time, repeat = levelSelect(current_level)
    time.sleep(2)
    my_list = [[2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6]]
    screen.refresh()
    time.sleep(1)
    curses.flushinp()
    direction = 1

    
  ###CHECK MOVING ENEMIES
#   for i in moving_enemy_list:
#     for j in my_list:
#       if i[0] == j[0] and i[1] == j[1]:
#         repeat, lives = gameOver(enemy_list, apple_list, money_list, my_list)
    
  
  

  q, direction, exitGame = captureMove(direction)


curses.endwin()