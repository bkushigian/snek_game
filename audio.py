from os import path

try:
    import pygame as pg
    import pygame.mixer as mixer
    WE_HAVE_PYGAME = True
except ImportError:
    print "Couldn't import pygame"
    WE_HAVE_PYGAME = False

MEDIA = 'media'
class Audio(object):
    def __init__(self):
        if WE_HAVE_PYGAME:
            pg.init()
            mixer.init()
            mixer.music.load(path.join(MEDIA, 'music.wav'))

            self.chomp    = mixer.Sound(path.join(MEDIA, 'chomp.wav'   ))
            self.money    = mixer.Sound(path.join(MEDIA, 'money.wav'   ))
            self.life     = mixer.Sound(path.join(MEDIA, 'life.wav'    ))
            self.block    = mixer.Sound(path.join(MEDIA, 'block.wav'   ))
            self.gameover = mixer.Sound(path.join(MEDIA, 'gameOver.wav'))
            self.levelwin = mixer.Sound(path.join(MEDIA, 'levelwin.wav'))
            
            chomp.set_volume(.8)
    def audio_menu(self):
        pass
        
