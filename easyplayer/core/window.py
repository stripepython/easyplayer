"""
Easy Player window class module.
"""

import sys
import os
from typing import Optional, Tuple, Callable, Any

import pygame
from pygame import constants

from easyplayer.core.event import Event
from easyplayer.core.saver import queue, SpriteQueue
from easyplayer.core.styles import normal, StyleType
from easyplayer.exceptions import EasyPlayerHandleError

__all__ = ['Window']


class Window(object):
    def __init__(self, title: Optional[str] = '', size: Optional[Tuple[int, int]] = (640, 480),
                 icon: Optional[str] = None, style: StyleType = normal, fps: int = 60,
                 on_center: bool = False, window_pos: Optional[Tuple[int, int]] = None,
                 vsync: bool = False, depth: int = 0):
        """
        Easy Player window object.
        
        :param title: Window title.
        :param size: Window size.
        :param icon: Window favicon, support PNG, JPEG, BMP...
        :param style: The style of window.
        :param fps: FPS.
        :param on_center: Whether window is on the center of screen.
        :param window_pos: Window position.
        :param vsync: Vsync.
        :param depth: Depth.
        """
        if on_center:
            os.environ['SDL_VIDEO_CENTERED'] = '1'
        if window_pos:
            x, y = window_pos
            os.environ['SDL_VIDEO_WINDOW_POS'] = f'{x},{y}'
            del x, y
        del on_center, window_pos  # Clear namespace
        self._pg = pygame
        self._init()
        
        self._pg_display = self._pg.display
        self._pg_load = self._pg.image.load
        
        self._title = title
        self._size = size
        
        self._flag = style.style
            
        self.width, self.height = size
        self.screen = self._pg_display.set_mode((self.width, self.height), self._flag, depth=depth, vsync=vsync)
        self._pg_display.set_caption(self._title)
        
        if icon:
            icon_surface = self._pg_load(icon)
            self._pg_display.set_icon(icon_surface)
            
        self._clock = self._pg.time.Clock()
        self._fps = fps
        self._sprites = SpriteQueue()  # Create queue
        
        self._event = Event()
        
        # Define default callbacks
        _empty_func = lambda: None
        self._when_mouse_down = _empty_func
        self._when_mouse_up = _empty_func
        self._when_key_down = _empty_func
        self._when_key_up = _empty_func
        self._when_mouse_move = _empty_func
        self._when_draw = _empty_func
        self._when_close = self.destroy
        self._when_resize = _empty_func
        self._when_active = _empty_func
        
        queue.append(self)
        
    def __str__(self):
        return f'Window(title={self.title}, size={self._pg_display.get_window_size()})'
        
    def _init(self):
        """
        Init all of pygame.
        
        :return: None
        """
        self._pg.init()
        self._pg.mixer.init()
        self._pg.font.init()
        
    def destroy(self, status: int = 0):
        """
        Close window and exit program.
        
        :param status: Exit status.
        :return: None
        """
        self._pg.quit()
        self._pg.mixer.quit()
        sys.exit(status)
        
    def update(self):
        """
        Update screen image.
        
        :return: None
        """
        self._pg_display.update()
        
    def when_mouse_down(self, func: Callable[[], Any]):
        """
        A decorator to decorate a callback function when mouse down.

        :param func: Callback function.
        :return: None
        """
        self._when_mouse_down = func

    def when_mouse_up(self, func: Callable[[], Any]):
        """
        A decorator to decorate a callback function when mouse up.

        :param func: Callback function.
        :return: None
        """
        self._when_mouse_up = func
        
    def when_mouse_move(self, func: Callable[[], Any]):
        """
        A decorator to decorate a callback function when mouse is moving.

        :param func: Callback function.
        :return: None
        """
        self._when_mouse_move = func
        
    def when_key_down(self, func: Callable[[], Any]):
        """
        A decorator to decorate a callback function when key down.

        :param func: Callback function.
        :return: None
        """
        self._when_key_down = func
        
    def when_key_up(self, func: Callable[[], Any]):
        """
        A decorator to decorate a callback function when key up.

        :param func: Callback function.
        :return: None
        """
        self._when_key_up = func
        
    def when_draw(self, func: Callable[[], Any]):
        """
        A decorator to decorate a callback function when update screen.

        :param func: Callback function.
        :return: None
        """
        self._when_draw = func
        
    def when_close(self, func: Callable[[], Any]):
        """
        A decorator to decorate a callback function when close window.
        
        Default callback is Window.destroy(0)

        :param func: Callback function.
        :return: None
        """
        self._when_close = func
        
    def when_resize(self, func: Callable[[], Any]):
        """
        A decorator to decorate a callback function when resize window.

        :param func: Callback function.
        :return: None
        """
        self._when_resize = func
        
    def when_active(self, func: Callable[[], Any]):
        """
        A decorator to decorate a callback function when active window.

        :param func: Callback function.
        :return: None
        """
        self._when_active = func
        
    def _event_handler(self, event: pygame.event.Event):
        """
        Parser and do event.
        
        :param event: Pygame event.
        :return: None
        """
        self._event = Event(event)
        if self._event.mouse_down:
            self._when_mouse_down()
        elif self._event.mouse_up:
            self._when_mouse_up()
        elif self._event.key_up:
            self._when_key_up()
        elif self._event.key_down:
            self._when_key_down()
        elif self._event.mouse_moving:
            self._when_mouse_move()
        elif self._event.resizing:
            self._when_resize()
        elif self._event.active:
            self._when_active()
        
    def show(self, escape_quit: bool = False):
        """
        Show and update this window.
        Start main loop.
        
        Like this:
        
        >>> import easyplayer as ep
        >>> window = ep.Window()
        >>> if __name__ == '__main__':
        >>>    window.show()
        
        :param escape_quit: Press Escape to exit.
        :return: None
        """
        while True:
            self._clock.tick(self._fps)
            self.screen.fill((255, 255, 255))   # White style
            for sprite in self._sprites:   # Draw packed sprites
                sprite.show()
            self._when_draw()
            
            for event in pygame.event.get():
                if event.type == constants.QUIT:
                    self._when_close()
                if escape_quit and event.type == constants.KEYDOWN:
                    if event.key == constants.K_ESCAPE:
                        self._when_close()
                self._event_handler(event)
              
            self.update()
            
    @property
    def event(self):
        """
        Window event.
    
        :return: Window event.
        """
        return self._event
    
    @property
    def mouse(self):
        """
        Create a mouse object of this window and return it.
        
        :return: Mouse object of this window.
        """
        return _Mouse()
    
    @property
    def sprites(self):
        """
        The queue of sprites.
        
        :return: The queue of sprites.
        """
        return self._sprites
    
    @property
    def hwnd(self):
        """
        The handle of this window.
        Information about the current windowing system
        
        In some operating systems, getting handle is not supported.
        
        :raise: EasyPlayerHandleError
        :return:
        """
        try:
            return self._pg_display.get_wm_info()['window']
        except KeyError:
            raise EasyPlayerHandleError('Getting hwnd is not supported')
        
    @property
    def title(self):
        return self._pg_display.get_caption()
    
    @title.setter
    def title(self, set_title: str):
        self._pg_display.set_caption(set_title)
        
    @property
    def size(self):
        return self._pg_display.get_window_size()
    
    @property
    def fps(self):
        return self._fps
    
    @fps.setter
    def fps(self, set_fps: int):
        self.set_fps(set_fps)
        
    def set_fps(self, fps: int):
        """
        Set FPS of this window.
        
        :param fps: FPS.
        :return: None
        """
        self._fps = fps
        
    def add_sprite(self, sprite):
        """
        Add a sprite.
        
        With Sprite.pack() has the same effect.
        
        :param sprite: Sprite.
        :return: None
        """
        self._sprites.append(sprite)
        
    def clear(self):
        """
        Clear this window.
        
        :return: None
        """
        self.screen.fill((255, 255, 255))
    
    
class _Mouse(object):
    def __init__(self):
        """
        Mouse class.
        """
        self._pg_mouse = pygame.mouse
        
    def __str__(self):
        return 'Mouse()'
        
    @property
    def pos(self):
        return self._pg_mouse.get_pos()
    
    @pos.setter
    def pos(self, set_pos: Tuple[int, int]):
        self._pg_mouse.set_pos(set_pos)
        
    @property
    def trail(self):
        """
        Get a series of actions of the mouse before this.
        
        Output instance:
        
        >>> [(0, 0), (3, 5), (14, 17), (22, 20)]
        
        :return: A series of actions of the mouse before this.
        """
        return self._pg_mouse.get_rel()
    
    def show(self):
        """
        Show cursor.
        
        :return: None
        """
        self._pg_mouse.set_visible(True)
        
    def hide(self):
        """
        Hide cursor.

        :return: None
        """
        self._pg_mouse.set_visible(False)
