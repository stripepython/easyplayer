"""
Easy Player can help you quickly build a game or simple GUI interface.

How to use:

>>> import easyplayer as ep

Such as:

>>> import easyplayer as ep
>>> window = ep.Window()
>>> sprite = ep.Sprite('xxx.png')
>>> sprite.pack()
>>> window.show()

Easy Player encapsulates pygame2.1, so you do not have to learn the PyGame API.
"""
__all__ = ['version', 'Window', 'Sprite', 'Background', 'Label', 'Font', 'Canvas', 'Pen', 'Video',
           'Camera', 'ColorModes', 'keys', 'styles', 'Screenshot', 'save_screenshot', 'Player',
           'play_sound', 'Timer', 'timer', 'recorder', 'Scrap', 'scrap_types', 'WebView', 'cs',
           'ClipBoard', 'print_screen', 'vectors', 'Color', 'Entry', 'sleep', 'error', 'random',
           'InWindow', 'RichText', 'Calendar', 'install_requirements', 'VariableManager', 'Screencap',
           'CloneManager', 'Bar', 'LBCoordinate', 'LTCoordinate', 'NormalCoordinate', 'chatters',
           'parse_coordinate', 'Translator', 'languages', 'JSEngines', 'speak', 'SpeakEngine',
           'ScreencapEncodings']

import os

try:
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'true'  # hide support prompt
except os.error:
    pass

from warnings import warn
from easyplayer.exceptions import EasyPlayerWarning, EasyPlayerError as error

from pygame.version import vernum

if vernum.major != 2 or vernum.minor != 1:
    warn_info = EasyPlayerWarning('Pygame version may cause problems')
    warn(warn_info)

# import API
import random

import pygame.math as vectors

from easyplayer import version

__version__ = version.version.get_string()
__author__ = 'stripe-python'

from easyplayer.core.window import Window
from easyplayer.core.widgets.sprite import Sprite
from easyplayer.core.widgets.background import Background
from easyplayer.core.widgets.label import Label, Font
from easyplayer.core.widgets.canvas import Canvas, Pen
from easyplayer.core.widgets.video import Video
from easyplayer.core.widgets.bar import Bar
try:
    from easyplayer.core.widgets.camera import Camera, ColorModes
except error:
    Camera = ColorModes = None
from easyplayer.core.widgets.entry.entry import Entry
from easyplayer.core.event import keys
import easyplayer.core.styles as styles

from easyplayer.utils.screenshot import Screenshot, save_screenshot
from easyplayer.utils.screencap import Screencap, ScreencapEncodings
from easyplayer.utils.music import Player, play_sound
from easyplayer.utils.timer import Timer, sleep
from easyplayer.utils.record import recorder
from easyplayer.utils.scrap import Scrap, scrap_types
from easyplayer.utils.color import Color
from easyplayer.utils.install import install_requirements
from easyplayer.utils.managers import VariableManager, CloneManager
from easyplayer.utils.coordinate import LTCoordinate, LBCoordinate, NormalCoordinate, parse_coordinate

from easyplayer.utils import cs

from easyplayer.utils.senior.translate import Translator, languages, JSEngines
from easyplayer.utils.senior.speak import speak, SpeakEngine
from easyplayer.utils.senior import chatter as chatters

import sys

if sys.platform == 'win32':
    from easyplayer.utils.wintools.browser import WebView
    from easyplayer.utils.wintools.printscreen import print_screen
    from easyplayer.utils.wintools.clipboard import ClipBoard
    from easyplayer.utils.wintools.inwindow import InWindow
    from easyplayer.utils.wintools.richtext import RichText
    from easyplayer.utils.wintools.calendar import Calendar
else:
    from easyplayer.exceptions import EasyPlayerOSError
    
    class _raise_error(object):
        @staticmethod
        def _raise():
            raise EasyPlayerOSError('Only supported Windows OS')
        
        def __init__(self, *_, **__):
            self._raise()
            
        def __getattr__(self, item):
            self._raise()
    
    WebView = _raise_error
    print_screen = _raise_error
    ClipBoard = _raise_error
    InWindow = _raise_error
    RichText = _raise_error
    Calendar = _raise_error


timer = Timer()  # Create a timer object for easy use.
