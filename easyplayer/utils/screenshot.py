import pygame

from easyplayer.core.saver import queue
from easyplayer.exceptions import EasyPlayerSaverError
from easyplayer.core.widgets.sprite import Sprite


__all__ = ['Screenshot', 'save_screenshot']


class Screenshot(object):
    def __init__(self):
        if not queue:
            raise EasyPlayerSaverError('please created a game first')
        self._game = queue[-1]

    def save(self, save_path='screenshot.png'):
        pygame.image.save(self._game.screen, save_path)
        
    def load_sprite(self, save_path='screenshot.png'):
        self.save(save_path)
        return Sprite(save_path)
        

def save_screenshot(save_path='screenshot.png'):
    Screenshot().save(save_path)
