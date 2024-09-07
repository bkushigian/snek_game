class Drawable(object):
    '''The default drawable mixin. This has a simple interface draw() that draws
    to screen.
    '''
    def __init__(self, screen):
        self.screen = screen
        pass

    def draw(self):
        pass
