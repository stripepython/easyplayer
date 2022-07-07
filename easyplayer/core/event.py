"""
Easy Player event tools.
"""

from typing import Optional, Union

from pygame.event import EventType
from pygame.locals import *
from pygame import constants

__all__ = ['Event', 'keys']


class _EmptyEvent(object):
    """
    Empty event.
    """
    type = None
    button = None
    key = None
    unicode = None
    gain = None
    state = None
    w = None
    h = None
    size = None


class Event(object):
    def __init__(self, event: Optional[EventType] = None):
        """
        Easy Player event parser.
        Used to parser pygame events.
        
        :param event: Pygame event.
        """
        if event is None:
            event = _EmptyEvent()
        self._event = event
        
    def __getitem__(self, item):
        return getattr(self._event, item)
    
    @property
    def mouse_down(self):
        """
        Virtual property, check whether the mouse is pressed.
        
        :return: Whether the mouse is pressed.
        """
        return self._event.type == MOUSEBUTTONDOWN
    
    @property
    def mouse_up(self):
        """
        Virtual property, check whether the mouse is released.

        :return: Whether the mouse is released.
        """
        return self._event.type == MOUSEBUTTONUP
    
    @property
    def key_down(self):
        """
        Virtual property, check whether any keys is down.

        :return: Whether any keys is down.
        """
        return self._event.type == KEYDOWN
    
    @property
    def key_up(self):
        """
        Virtual property, check whether any keys is up.

        :return: Whether any keys is down.
        """
        return self._event.type == KEYUP
    
    @property
    def mouse_moving(self):
        """
        Virtual property, check whether any keys is moving.

        :return: Whether any keys is moving.
        """
        return self._event.type == MOUSEMOTION
    
    @property
    def press_left_button(self):
        """
        Virtual property, check whether the left key is pressed.

        :return: Whether the left key is pressed.
        """
        if self.mouse_down:
            return self._event.button == 1
        return False
    
    @property
    def press_middle_button(self):
        """
        Virtual property, check whether the middle key is pressed.

        :return: Whether the middle key is pressed.
        """
        if self.mouse_down:
            return self._event.button == 2
        return False
    
    @property
    def press_right_button(self):
        """
        Virtual property, check whether the right key is pressed.

        :return: Whether the right key is pressed.
        """
        if self.mouse_down:
            return self._event.button == 3
        return False
    
    @property
    def active(self):
        """
        Virtual property that is true when the mouse is moved into or out of a window.
        
        :return: Whether the mouse moves in or out of the window.
        """
        return self._event.type == ACTIVEEVENT
    
    @property
    def gain(self):
        """
        Virtual attribute, which is none when the active event is None.
        When the active event is triggered, if the mouse moves into the window is True, otherwise it is False.
        
        :return: Whether the mouse moves into the window.
        """
        if self.active:
            try:
                return bool(self._event.gain)
            except AttributeError:
                return None
        return None
    
    @property
    def state(self):
        """
        Virtual attribute, which is none when the active event is None.
        When the active event is triggered, it is True if the window is activated; otherwise, it is False.

        :return: Whether the window is active.
        """
        if self.active:
            try:
                return bool(self._event.state)
            except AttributeError:
                return None
        return None
    
    @property
    def resizing(self):
        """
        Virtual property that is true when window is resizing.
        
        :return: Is window resizing.
        :rtype: bool
        """
        return self._event.type == VIDEORESIZE
    
    @property
    def window_size(self):
        """
        Virtual attribute, which is none when the resizing event is None.
        When the resizing event is triggered, the window size is returned.

        :return: The window size.
        """
        if self.resizing:
            return self._event.size
        return None
    
    @property
    def window_width(self):
        """
        Virtual attribute, which is none when the resizing event is None.
        When the resizing event is triggered, the window width is returned.

        :return: The width of the window.
        """
        if self.resizing:
            return self._event.w
        return None
    
    @property
    def window_height(self):
        """
        Virtual attribute, which is none when the resizing event is None.
        When the resizing event is triggered, the window height is returned.

        :return: The height of the window.
        """
        if self.resizing:
            return self._event.h
        return None
    
    def is_down(self, key: Union[int, str]):
        """
        Check if a key is pressed.
        
        :param key: Key's code or char.
        :return: Whether to press this key.
        """
        if self.key_down:
            if isinstance(key, int):
                return self._event.key == key
            if isinstance(key, str):
                return keys.get(key) == self._event.key
            return False
        return False
    
    def is_up(self, key: Union[int, str]):
        """
        Check if a key is released.

        :param key: Key's code or char.
        :return: Whether to release this key.
        """
        if self.key_up:
            if isinstance(key, int):
                return self._event.key == key
            if isinstance(key, str):
                return keys.get(key) == self._event.key
            return False
        return False
    
    @property
    def char(self):
        """
        Virtual attribute to get the character form of the current key.
        Return to none when a key is not pressed or released.
        
        :return: The character form of the current key.
        """
        if not (self.key_up or self.key_down):
            return None
        return self._event.unicode


def _get_keys():
    dct = constants.__dict__.copy()   # Get key list
    res = {}
    for key, value in dct.items():
        if key.startswith('K_'):
            key = key.replace('K_', '').lower()
            res[key] = value
    return res


keys = _get_keys()
del constants, _get_keys  # Clear namespace
