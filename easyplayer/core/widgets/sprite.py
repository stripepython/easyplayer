"""
Easy Player base widget module.
"""

import math  # Need trigonometric functions
from typing import Optional, Tuple, Callable, Any

import pygame

from easyplayer.core.saver import queue
from easyplayer.exceptions import EasyPlayerSaverError

__all__ = ['Sprite']


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image: str, size: Optional[Tuple[int, int]] = None, convert_alpha: bool = False):
        """
        Basic role component class.
        
        It inherit pygame.sprite.Sprite.
        This means that it has good compatibility with pygame.
        
        :param image: Image path, support JPEG, PNG, GIF, BMP, PCX, TGA, TIF, LBM, PBM, XPM, SVG, WEBP
        :param size: If this parameter is set, the size of the picture is automatically scaled.
        :param convert_alpha: Convert to RGBA.
        """
        super().__init__()
        if not queue:
            raise EasyPlayerSaverError('please create a game first')
        self._game = queue[-1]
        self._screen = self._game.screen
        self._screen_rect = self._screen.get_rect()
        self._path = image
        self._angle = 0
        
        self.image = pygame.image.load(image)
        if size:
            self.image = pygame.transform.scale(self.image, size)  # Auto scale
        if convert_alpha:
            self.image = self.image.convert_alpha()
            
        self.rect = self.image.get_rect()
        self.size = (self.rect.width, self.rect.height)
        self.width, self.height = self.size
        self.update = self.show
        
        _empty_func = lambda: None
        self._when_click_me = _empty_func
        
    def __str__(self):
        return f'Sprite(image={self._path}, size={self.size})'
    
    def __copy__(self):
        """
        Create a clone.
        
        :return: A clone.
        """
        sprite = Sprite(image=self._path, size=self.size)
        sprite.rect = self.rect.copy()
        sprite.image = self.image.copy()
        return sprite
    
    clone = copy = __copy__
    
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
        
    @property
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self, set_angle: float):
        self.rotate(set_angle)
        
    def rotate(self, angle: float, image_rotate: bool = True):
        """
        Counterclockwise rotation.
        
        :param angle: Angle.
        :param image_rotate: Rotate image.
        :return: None
        """
        self._angle = angle
        if image_rotate:
            self.image = pygame.transform.rotate(self.image, angle)
            self.rect = self.image.get_rect()
        
    def when_click_me(self, func: Callable[[], Any]):
        """
        A decorator to decorate a callback function when click this sprite.

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

    def collide_left_edge(self):
        """
        Judge whether it collides left edge.
        
        :return: Whether it collides left edge.
        """
        return self.rect.left <= 0
    
    def collide_right_edge(self):
        """
        Judge whether it collides right edge.

        :return: Whether it collides right edge.
        """
        return self.rect.right >= self._screen_rect.width

    def collide_top_edge(self):
        """
        Judge whether it collides top edge.

        :return: Whether it collides top edge.
        """
        return self.rect.top <= 0
       
    def collide_bottom_edge(self):
        """
        Judge whether it collides bottom edge.

        :return: Whether it collides bottom edge.
        """
        return self.rect.bottom >= self._screen_rect.height
    
    def collide_edge(self):
        """
        Judge whether it collides any edges.

        :return: Whether it collides any edges.
        """
        return self.collide_left_edge() or self.collide_right_edge() or self.collide_top_edge() or self.collide_bottom_edge()
        
    def show(self):
        """
        Update and show this sprite in screen.
        
        :return: None
        """
        self._screen.blit(self.image, self.rect)
        if self.collide_mouse() and self._game.event.mouse_down:
            self._when_click_me()
            
    def pack(self):
        """
        Pack this sprite object.
        
        :return: None
        """
        self._game.add_sprite(self)
        
    def forward(self, length: int):
        """
        Let the sprite move in its own direction.
        
        Warning: this is the test function, it is unstable!
        
        :param length: Length of movement.
        :return: None
        """
        x, y = self.pos
        r = math.radians(self._angle)
        self.pos = x + length * math.cos(r), y + length * math.sin(r)
            
    def rebound_if_collide_edge(self):
        """
        Rebound if collide any edges.
        
        Warning: this is the test function, it is unstable!
        
        :return: None
        """
        if self.collide_edge():
            self._angle = 180 - self._angle
            
    rice = rebound_if_collide_edge
