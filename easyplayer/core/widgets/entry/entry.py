"""
Easy Player entry widget.
Implemented a simple input box.
This is the test function, it is unstable!
"""

from typing import Tuple, Callable, Any

import pygame

from easyplayer.core.widgets.label import Label, Font
from easyplayer.core.saver import queue
from easyplayer.exceptions import EasyPlayerSaverError, EasyPlayerTextTooLongError
from easyplayer.utils.color import ColorType

# define default colors
_color_inactive = pygame.Color('lightskyblue3')
_color_active = pygame.Color('dodgerblue2')

__all__ = ['Entry']


class Entry(object):
    def __init__(self, default_text: str = '', font: Font = Font(), size: Tuple[int, int] = (140, 32),
                 antialias: bool = True, foreground: ColorType = (0, 0, 0), color_active: ColorType = _color_active,
                 color_inactive: ColorType = _color_inactive, width: int = 2, can_longer: bool = True):
        """
        Easy Player entry widget.
        Implemented a simple input box.
        
        Warning: this is the test function, it is unstable!
        
        :param default_text: Default text.
        :param font: Font object, for detailed documents, see easyplayer.core.widgets.label.Font
        :param size: Font size.
        :param antialias: Is antialias.
        :param foreground: Foreground text color.
        :param color_active: Bar color when active.
        :param color_inactive: Bar color when inactive.
        :param width: The width of the width.
        :param can_longer: Whether it can be extended. If choose False, An error will be reported when the text exceeds the range.
        """
        if not queue:
            raise EasyPlayerSaverError('please create a game first')
        self._game = queue[-1]
        self._screen = self._game.screen
        
        self._label = Label(default_text, font, antialias, foreground)
        self.rect = pygame.rect.Rect(0, 0, *size)
        self._label.rect.x, self._label.rect.y = self.rect.x, self.rect.y
        self._width = width
        self._can_longer = can_longer
        
        self.active = False
        self._color = color_inactive
        self._color_active = color_active
        self._color_inactive = color_inactive
        
        empty_func = lambda: None
        self._when_enter = empty_func
        self._when_active = empty_func
        
        self.text = default_text
        
    @property
    def pos(self):
        return self.rect.x, self.rect.y
    
    @pos.setter
    def pos(self, set_pos: Tuple[int, int]):
        self._label.pos = set_pos
        self.rect.x, self.rect.y = set_pos

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, set_x: int):
        self._label.x = set_x
        self.rect.x = set_x

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, set_y: int):
        self._label.y = set_y
        self.rect.y = set_y
        
    def when_enter(self, func: Callable[[], Any]):
        """
        A decorator to decorate a callback function when press enter.
        
        :param func: Callback function.
        :return: None
        """
        self._when_enter = func
        
    def when_active(self, func: Callable[[], Any]):
        """
        A decorator to decorate a callback function when active.

        :param func: Callback function.
        :return: None
        """
        self._when_active = func
        
    def get(self):
        """
        A function to get text.
        
        :return: Text in this entry box.
        """
        return self.text
    
    def pack(self):
        """
        Pack this entry object.
        
        :return: None
        """
        self._game.add_sprite(self)
        
    def show(self):
        """
        A show function.
        
        If you choose can_longer=False, it will raise EasyPlayerTextTooLongError when the text exceeds the range.
        
        :raise: EasyPlayerTextTooLongError
        :return: None
        """
        self._label.set_text(self.text)
        self._label.show()
        if self._can_longer:
            w = max(self.rect.width, self._label.image.get_width() + 10)
            self.rect.width = w
        else:
            if (self._label.image.get_width() + 10) > self.rect.width:
                raise EasyPlayerTextTooLongError('Input too long')
        pygame.draw.rect(self._screen, self._color, self.rect, self._width)
        
        event = self._game.event
        
        if event.mouse_down:
            if self.rect.collidepoint(self._game.mouse.pos):
                self.active = not self.active
            else:
                self.active = False
            self._color = self._color_active if self.active else self._color_inactive
            self._when_active()
        
        if event.key_down:
            if event.is_down(301):
                return
            if self.active:
                if event.is_down(pygame.K_RETURN):
                    self._when_enter()
                elif event.is_down(pygame.K_BACKSPACE):
                    self.text = self.text[:-1]
                else:
                    self.text += event.char
