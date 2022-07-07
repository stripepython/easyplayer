"""
Easy Player calendar widget module.

This code has syntax errors in pycharm, but it runs normally.
"""

import sys
import ctypes
from typing import Tuple

from easyplayer.exceptions import EasyPlayerOSError, EasyPlayerSaverError
from easyplayer.core.saver import queue

if sys.platform != 'win32':
    raise EasyPlayerOSError('Only supported Windows OS')

import clr

try:
    # Add reference
    clr.AddReference('System.Windows.Forms')
    clr.AddReference('System.Drawing')
    clr.AddReference('System')
except OSError:
    raise EasyPlayerOSError('Only supported Windows OS') from None
from System.Windows.Forms import MonthCalendar    # Pycharm syntax error

_user32 = ctypes.windll.user32

__all__ = ['Calendar']


class Calendar(object):
    def __init__(self, size: Tuple[int, int] = (320, 240)):
        """
        Easy Player calendar widget.
        
        Warning: available only on Windows system.
        
        :param size: The size of this widget.
        """
        if not queue:
            raise EasyPlayerSaverError('please created a game first')
        self._game = queue[-1]
        
        self._ca = MonthCalendar()
        self._ca_hwnd = int(str(self._ca.Handle))
        
        _user32.SetParent(self._ca_hwnd, self._game.hwnd)
        self.x, self.y = 0, 0
        self.width, self.height = size
        self._move()
        
    def _move(self):
        """
        Move the position of this widget.
        
        :return: None
        """
        _user32.MoveWindow(self._ca_hwnd, self.x, self.y, self.width, self.height, True)

    def resize(self, size: Tuple[int, int]):
        """
        Resize this widget.
        
        :param size: The size of this widget.
        :return: None
        """
        self._ca.Width, self._ca.Height = size
        self.width, self.height = size
        
    @property
    def pos(self):
        return self.x, self.y
    
    @pos.setter
    def pos(self, set_pos: Tuple[int, int]):
        self.x, self.y = set_pos
        self._move()
