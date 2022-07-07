"""
Easy Player label widget and font class.
"""

from typing import Union, Tuple, Callable, Any

import pygame

from easyplayer.core.saver import queue
from easyplayer.exceptions import EasyPlayerSaverError

__all__ = ['Font', 'Label']


class Font(object):
    def __init__(self, font_path: str = None, size: int = 25):
        """
        Easy Player font object.
        Load from a font file.
        
        Support TTF, OTF and EOT.
        
        :param font_path: Font file path.
        :param size: Font size.
        """
        pygame.font.init()
        self.font = pygame.font.Font(font_path, size)
        
    @staticmethod
    def from_system(name: str, size: int = 25, bold: bool = False, italic: bool = False):
        """
        Create a Font object from system font.
        
        :param name: The name of this system font, such as "Times" or "simsun".
        :param size: Font size.
        :param bold: Bold.
        :param italic: Italic.
        :return: A Font object from this system font.
        """
        res = Font()
        res.font = pygame.font.SysFont(name, size, bold, italic)
        return res
    
    @staticmethod
    def get_fonts():
        """
        Get a list of system font names.

        :return: The list of all found system fonts.
        """
        return pygame.font.get_fonts()


class Label(pygame.sprite.Sprite):
    def __init__(self, text: str = '', font: Font = Font(), antialias: bool = True,
                 color: Union[Tuple[int, int, int], Tuple[int, int, int, int], pygame.color.Color] = (0, 0, 0)):
        """
        Easy Player label widget.
        
        It inherit pygame.sprite.Sprite.
        This means that it has good compatibility with pygame.
        
        :param text: Label text.
        :param font: The font of this label.
        :param antialias: Whether antialias.
        :param color: The color of the text.
        """
        super().__init__()
        if not queue:
            raise EasyPlayerSaverError('please create a game first')
        self._game = queue[-1]
        self._screen = self._game.screen
        
        self.font = font
        self.text = str(text)
        self.color = color
        self.antialias = antialias
        self._init()
        
        self.update = self.show
        
        _empty_func = lambda: None
        self._when_click_me = _empty_func
        
    def __str__(self):
        return f'Label(text={self.text})'
    
    def __copy__(self):
        """
        Create a same label.
        
        :return: A same label object.
        """
        res = Label(self.text, self.font, self.antialias, self.color)
        res.image = self.image.copy()
        res.rect = self.rect.copy()
        return res
    
    copy = clone = __copy__
    
    def _init(self):
        self.image = self.font.font.render(self.text, self.antialias, self.color)
        self.rect = self.image.get_rect()

    @property
    def pos(self):
        return self.rect.x, self.rect.y

    @pos.setter
    def pos(self, set_pos: Tuple[int, int]):
        self.rect.x, self.rect.y = set_pos

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, set_x: int):
        self.rect.x = set_x

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, set_y: int):
        self.rect.y = set_y

    def when_click_me(self, func: Callable[[], Any]):
        """
        A decorator to decorate a callback function when click this label.

        :param func: Callback function.
        :return: None
        """
        self._when_click_me = func

    def collide_other(self, sprite: pygame.sprite.Sprite):
        """
        Determine whether it collides with other sprite.

        Warning: Collision detection method rectangular object based on sprite. Possible error.

        :param sprite: Other sprite.
        :return: Whether it collides with other sprite.
        """
        return pygame.sprite.collide_rect(self, sprite)

    def collide_mouse(self):
        """
        Determine whether it collides with mouse.

        Warning: Collision detection method rectangular object based on sprite. Possible error.

        :return: Whether it collides with mouse.
        """
        point = pygame.mouse.get_pos()
        return self.rect.collidepoint(point)

    def collide_point(self, x: int, y: int):
        """
        Determine whether it collides with a point.

        Warning: Collision detection method rectangular object based on sprite. Possible error.

        :param x: X coordinate.
        :param y: Y coordinate.
        :return: Whether it collides with this point.
        """
        return self.rect.collidepoint(x, y)

    def show(self):
        """
        Show this label widget.
        
        :return: None
        """
        self._screen.blit(self.image, self.rect)
        if self.collide_mouse() and self._game.event.mouse_down:
            self._when_click_me()

    def pack(self):
        """
        Pack this label object.
        
        :return: None
        """
        self._game.add_sprite(self)
        
    def set_text(self, text: str):
        """
        Set the text of this label.
        
        :param text: Text content.
        :return: None
        """
        self.text = str(text)
        rct = self.rect.copy()
        self._init()
        self.rect.x, self.rect.y = rct.x, rct.y
        
    def set_style(self, font: Font, antialias: bool = True,
                  color: Union[Tuple[int, int, int], Tuple[int, int, int, int], pygame.color.Color] = (0, 0, 0)):
        """
        Set the style of this label.
        
        :param font: The font of this label.
        :param antialias: Whether antialias.
        :param color: The color of the text.
        :return: None
        """
        self.font = font
        self.color = color
        self.antialias = antialias
        self._init()
