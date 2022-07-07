"""
Easy Player clipboard tool module.
"""

import sys

from easyplayer.exceptions import EasyPlayerOSError, EasyPlayerModuleError

if sys.platform != 'win32':
    raise EasyPlayerOSError('Only supported Windows OS')

try:
    import win32clipboard
    import win32con
except (ModuleNotFoundError, ImportError):
    class _raise_error(object):
        CF_UNICODETEXT = None
        
        @staticmethod
        def OpenClipboard():
            raise EasyPlayerModuleError('please install win32clipboard and win32con')
        
    win32clipboard = win32con = _raise_error
    
__all__ = ['ClipBoard']
    

class ClipBoard(object):
    def __init__(self):
        """
        Easy Player clipboard tool.
        
        Warning: available only on Windows system.
        """
        self._cf = win32con.CF_UNICODETEXT
    
    @property
    def text(self):
        win32clipboard.OpenClipboard()
        res = win32clipboard.GetClipboardData(self._cf)
        win32clipboard.CloseClipboard()
        return res
    
    @text.setter
    def text(self, set_text: str):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(self._cf, set_text)
        win32clipboard.CloseClipboard()
