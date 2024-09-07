from externs import *
from os      import path
from action  import Action

try:
    import pygame as pg
    import pygame.mixer as mixer
    we_have_pygame = True
except ImportError:
    print("Couldn't import pygame")
    we_have_pygame = False

class Audio(object):
    def __init__(self):
        self._audio_map = {}
        if we_have_pygame:
            pg.init()
            mixer.init()
            self.music = mixer.music
            self.add_music( 'Wanks1.wav')

            self.chomp    = self.add_audio( 'chomp.wav'   )
            self.money    = self.add_audio( 'money.wav'   )
            self.life     = self.add_audio( 'life.wav'    )
            self.block    = self.add_audio( 'block.wav'   )
            self.gameover = self.add_audio( 'gameOver.wav')
            self.levelwin = self.add_audio( 'levelWin.wav')
            
            self.chomp.set_volume(.7)
            

    def audio_menu(self):
        pass

    def get_audio(self, name):
        if name in self._audio_map:
            return self._audio_map[name]

    def play_audio(self, name):
        if name in self._audio_map:
            self._audio_map[name].play()
        
    def add_audio(self, filename, filepath = MEDIA):
        audiomap = self._audio_map
        name = filename.split('.')[0]
        if we_have_pygame:
            if name in audiomap:
                return None  # DEFAULT: Do not overwrite
            sound = mixer.Sound(path.join(filepath, filename))
            audiomap[name] = sound
            return sound

    def add_music(self, filename, filepath = MEDIA):
        if we_have_pygame:
            self.music.load(path.join(filepath, filename))

    def play_music(self, music = None, loops = 0, start = 0.0):
        if music:
            try:
                self.add_music(music)
            except Exception as e:
                pass
        self.music.play()

    def queue_music(self, filename):
        self.music.queue(filename)

    def fadeout_music(self, fadetime=3000):
        self.music.fadeout(fadetime)
        

            

        

        
