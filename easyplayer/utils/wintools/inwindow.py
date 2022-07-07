"""
Easy Player nested sub window widget module.
"""

import ctypes
import sys
from typing import Tuple, Union
import tkinter

from easyplayer.core.saver import queue
from easyplayer.exceptions import EasyPlayerOSError, EasyPlayerSaverError

if sys.platform != 'win32':
    raise EasyPlayerOSError('Only supported Windows OS')

_user32 = ctypes.windll.user32

__all__ = ['InWindow']


class InWindow(object):
    def __init__(self, hwnd: int, size: Tuple[int, int] = (320, 240)):
        """
        Easy Player nested sub window widget
        
        Warning: available only on Windows system.
        
        :param hwnd: Window's handle.
        :param size: The size of this widget.
        """
        if not queue:
            raise EasyPlayerSaverError('please create a game first')
        self._game = queue[-1]
        self._screen = self._game.screen
        
        self._game_hwnd = self._game.hwnd
        self._window_hwnd = hwnd
        self.x, self.y = 0, 0
        self.width, self.height = size
        
    def _move(self):
        """
        Move the position of this widget.
        
        :return: None
        """
        _user32.MoveWindow(self._window_hwnd, self.x, self.y)
        
    def pack(self):
        """
        Pack this widget.
        
        :return: None
        """
        _user32.SetParent(self._window_hwnd, self._game_hwnd)
        self._move()
        
    @property
    def pos(self):
        return self.x, self.y
    
    @pos.setter
    def pos(self, set_pos: Tuple[int, int]):
        self.x, self.y = set_pos
        self._move()
        
    @staticmethod
    def from_tk(tk: Union[tkinter.Widget, tkinter.Tk, tkinter.Toplevel]):
        """
        Create nested Tkinter window.
        
        :param tk: This Tkinter window.
        :return: Nested Tkinter window.
        """
        hwnd = tk.winfo_id()
        return InWindow(hwnd)
