"""
Easy Player webview widget module.

This code has syntax errors in pycharm, but it runs normally.
"""

import ctypes
import sys
from typing import Tuple, Callable, Any

from easyplayer.exceptions import EasyPlayerOSError, EasyPlayerSaverError, EasyPlayerModuleError
from easyplayer.core.saver import queue

if sys.platform != 'win32':
    raise EasyPlayerOSError('Only supported Windows OS')

import threading

try:
    import clr
except (ImportError, ModuleNotFoundError):
    raise EasyPlayerModuleError('please install clr') from None

try:
    # Add reference
    clr.AddReference('System.Windows.Forms')
    clr.AddReference('System.Threading')
except OSError:
    raise EasyPlayerOSError('Only supported Windows OS') from None
from System.Windows.Forms import *    # Pycharm syntax error
from System.Threading import Thread, ApartmentState, ThreadStart    # Pycharm syntax error

_app = Application  # Pycharm syntax error
_user32 = ctypes.windll.user32

class _Form(object):
    """
    Default form.
    """


__all__ = ['WebView']


class WebView(object):
    def __init__(self, size: Tuple[int, int] = (1200, 550), url: str = '',
                 script_errors_suppressed: bool = True, menu_enabled: bool = True):
        """
        Easy Player webview widget.
        
        Warning: available only on Windows system.
        
        :param size: Widget size.
        :param url: Default URL.
        :param script_errors_suppressed: Script errors suppressed.
        :param menu_enabled: Is the menu enabled.
        """
        if not queue:
            raise EasyPlayerSaverError('please created a game first')
        self._game = queue[-1]
        self._screen = self._game.screen

        self.width, self.height = size
        
        form = _Form()
        # Must use thread
        threading.Thread(target=self._get_web, args=(form, self.width, self.height)).start()
        
        while True:
            try:
                ie = form.web
                break
            except AttributeError:
                pass
                
        ie.ScriptErrorsSuppressed = script_errors_suppressed
        self.ie_hwnd = int(str(ie.Handle))
        self.x, self.y = 0, 0
        # Use win32api
        _user32.SetParent(self.ie_hwnd, self._game.hwnd)
        self._move()
        
        if url != '':
            ie.Navigate(url)
        self.ie = ie
        self.ie.IsWebBrowserContextMenuEnabled = menu_enabled
        self.ie.NewWindow += self._before_window
        
        self.url = url
        
    @staticmethod
    def _get_web(form: _Form, width: int, height: int):
        """
        Set the form attr.
        
        :param form: This form.
        :param width: Width.
        :param height: Height.
        :return: None
        """
        web = WebBrowser()   # Pycharm syntax error
        form.web = web
        web.Width = width
        web.Height = height
        
    def _before_window(self, sender, e):
        """
        A handler.
        
        :param sender: Sender.
        :param e: E.
        :return: None
        """
        href = sender.Document.ActiveElement.GetAttribute('href')
        self.set_url(href)
        e.Cancel = True
        
    def _move(self):
        _user32.MoveWindow(self.ie_hwnd, self.x, self.y, self.width, self.height, True)
        
    @property
    def pos(self):
        return self.x, self.y
    
    @pos.setter
    def pos(self, set_pos: Tuple[int, int]):
        self.x, self.y = set_pos
        self._move()

    def set_url(self, url: str):
        """
        Set the URL of this webview.
        
        :param url: URL.
        :return: None
        """
        self.url = url
        self.ie.Navigate(url)
        
    def show_url(self, func: Callable[[], Any]):
        """
        A decorator to decorate a callback function when change URL.
        
        Warning: this is the test function, it is unstable!

        :param func: Callback function.
        :return: None
        """
        self.ie.Navigating += func
        
    def resize(self, width: int, height: int):
        """
        Resize webview.
        
        :param width: Width.
        :param height: Height.
        :return: None
        """
        self.width, self.height = width, height
        self.ie.Width = width
        self.ie.Height = height
        
    def destroy(self):
        """
        Destroy this web view.
        
        :return: None
        """
        self.ie.Dispose()
        del self.ie
