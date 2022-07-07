from typing import Tuple

import pygame

from easyplayer.core.saver import queue
from easyplayer.exceptions import EasyPlayerSaverError
from easyplayer.utils.color import ColorType


class Bar(object):
    def __init__(self, width: int = 240, height: int = 30, border_width: int = 1,
                 proportion: float = 1.0, border_color: ColorType = (0, 0, 0), bar_color: ColorType = (255, 0, 0)):
        if not queue:
            raise EasyPlayerSaverError('please create a game first')
        self._game = queue[-1]
        self._screen = self._game.screen
        
        self.width, self.height = width, height
        self.x, self.y = 0, 0
        self.border_width = border_width
        self.proportion = proportion
        self._set_width()
        
        self.border_color = border_color
        self.bar_color = bar_color
        
    @property
    def pos(self):
        return self.x, self.y
    
    @pos.setter
    def pos(self, set_pos: Tuple[int, int]):
        self.x, self.y = set_pos
        self._set_width()
        
    def _set_width(self):
        self.rect_border = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        self.rect_bar = pygame.rect.Rect(self.x, self.y, self.width * self.proportion, self.height)
        
    def pack(self):
        self._game.add_sprite(self)
        
    def show(self):
        pygame.draw.rect(self._screen, self.bar_color, self.rect_bar)
        pygame.draw.rect(self._screen, self.border_color, self.rect_border, width=self.border_width)

    def set_proportion(self, proportion: float):
        if proportion < 0:
            proportion = 0
        self.proportion = proportion
        self._set_width()
        
    def resize(self, width: int, height: int):
        self.width, self.height = width, height
        self._set_width()
