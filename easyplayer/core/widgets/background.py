"""
Easy Player background widget.

Provide simple background functions.
"""

import pygame

from easyplayer.core.widgets.sprite import Sprite

__all__ = ['Background']


class Background(Sprite):
    def __init__(self, image: str, fullscreen: bool = True):
        """
        Easy Player background widget.
        
        It inherit easyplayer.core.widgets.sprite.Sprite.
        
        :param image: Background image path.
        :param fullscreen: Adaptive screen size.
        """
        super().__init__(image)
        self._screen_rect = self._screen.get_rect()
        self._fullscreen = fullscreen
        if fullscreen:
            self.image = pygame.transform.scale(self.image,
                                                (self._screen_rect.width,
                                                 self._screen_rect.height))
            self.rect = self.image.get_rect()
            
    def __copy__(self):
        """
        Create a same background.

        :return: The same background.
        """
        return Background(self._path, fullscreen=self._fullscreen)
    
    copy = clone = __copy__
    
    def __str__(self):
        return f'Background(image={self._path}, fullscreen={self._fullscreen})'
    
    def scroll_down(self, speed=4):
        """
        Scroll down background.
        
        :param speed: Scroll speed.
        :return: None
        """
        x, y = self.pos
        y += speed
        if y > self._screen_rect.height:
            y = -self._screen_rect.height
        self.pos = x, y
        
    def scroll_up(self, speed=4):
        """
        Scroll up background.

        :param speed: Scroll speed.
        :return: None
        """
        x, y = self.pos
        y -= speed
        if y < -self._screen_rect.height:
            y = self._screen_rect.height
        self.pos = x, y
        
    def scroll_left(self, speed=4):
        """
        Scroll left background.

        :param speed: Scroll speed.
        :return: None
        """
        x, y = self.pos
        x -= speed
        if x < -self._screen_rect.width:
            x = self._screen_rect.width
        self.pos = x, y

    def scroll_right(self, speed=4):
        """
        Scroll right background.

        :param speed: Scroll speed.
        :return: None
        """
        x, y = self.pos
        x += speed
        if x > self._screen_rect.width:
            x = -self._screen_rect.width
        self.pos = x, y
