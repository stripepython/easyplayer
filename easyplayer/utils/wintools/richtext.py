"""
Easy Player richtext widget module.

This code has syntax errors in pycharm, but it runs normally.
"""

import sys
from webbrowser import open as web_open
import ctypes
from typing import Tuple, Callable, Any

from easyplayer.exceptions import EasyPlayerOSError, EasyPlayerSaverError
from easyplayer.core.saver import queue

if sys.platform != 'win32':
    raise EasyPlayerOSError('Only supported Windows OS')

import clr

try:
    # Add references
    clr.AddReference('System.Windows.Forms')
    clr.AddReference('System.Drawing')
    clr.AddReference('System')
except OSError:
    raise EasyPlayerOSError('Only supported Windows OS') from None
from System.Windows.Forms import RichTextBox    # Pycharm syntax error
from System.Drawing import Font    # Pycharm syntax error
from System import String, Single    # Pycharm syntax error

_user32 = ctypes.windll.user32

__all__ = ['RichText']


class RichText(object):
    def __init__(self, font_name: str = 'Arial', font_size: int = 13,
                 size: Tuple[int, int] = (320, 240)):
        """
        Easy Player richtext widget.
        
        :param font_name: The name of the font.
        :param font_size: The name of the size.
        :param size: Widget size.
        """
        if not queue:
            raise EasyPlayerSaverError('please created a game first')
        self._game = queue[-1]
        
        self._font = Font(String(font_name), Single(font_size))
        self._rtf = RichTextBox()
        self._rtf.font = self._font
        
        self._rtf_hwnd = int(str(self._rtf.Handle))
        _user32.SetParent(self._rtf_hwnd, self._game.hwnd)
        self.x, self.y = 0, 0
        self.width, self.height = size
        self._move()
        
        self._when_open_url = web_open
        self._rtf.LinkClicked += self._open_url
        
    def _move(self):
        """
        Move this widget.
        
        :return: None
        """
        _user32.MoveWindow(self._rtf_hwnd, self.x, self.y, self.width, self.height, True)
        
    def load(self, rtf_file: str):
        """
        Load a RTF file.
        
        :param rtf_file: The path of the RTF file.
        :return: None
        """
        self._rtf.LoadFile(rtf_file)
        
    def _open_url(self, _, e):
        self._when_open_url(e.LinkText)
        
    def when_open_url(self, func: Callable[[str], Any]):
        """
        A decorator to decorate a callback function when open a URL.
        
        Default is webbrowser.open(url).

        :param func: Callback function.
        :return: None
        """
        self._when_open_url = func
        
    def resize(self, size: Tuple[int, int]):
        """
        Resize this widget.
        
        :param size: The size of this widget.
        :return: None
        """
        self._rtf.Width, self._rtf.Height = size
        self.width, self.height = size
