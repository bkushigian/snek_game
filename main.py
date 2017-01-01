import time
import random
from sys import exit
from os import path

# Local Imports
import audio
import board
import driver
import menu


def main():
    ''' Main function. Creates board, screen, etc. '''
    # Queue Intro Music!
    audio = audio.Audio()

    # First, create screen to check dimensions

    # Then, Create Main Menu to take user input

    # Launch Game!
    pass
    
# TODO: Where to put this?
# TODO: This is a dumb function signature
# TODO: This is a stupid fucking return value
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
