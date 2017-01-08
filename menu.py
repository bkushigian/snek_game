# TODO: This is directly copied from wyrm file -- make it pretty, make it work!

class Menu(object):
    # FIXME: Directly copied, lots of 'global' references that will not be
    # defined. 
    def audio(self):
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
