"""
Easy Player printscreen window tool moudle.
"""

import time
import tkinter as tk
from tkinter.messagebox import showinfo
import ctypes
from typing import Tuple

try:
    from PIL import Image, ImageGrab
except (ImportError, ModuleNotFoundError):
    from easyplayer.exceptions import EasyPlayerError
    
    class _raise_error(object):
        @staticmethod
        def grab(*args, **kwargs):
            raise EasyPlayerError('Please install pillow')
    
    Image = ImageGrab = _raise_error
    
import sys
if sys.platform != 'win32':
    from easyplayer.exceptions import EasyPlayerError

    raise EasyPlayerError('Only supported Windows OS')


__all__ = ['print_screen']
    

class _PrintScreenWindow(object):
    def __init__(self, save_path: str = 'grab.png', pos: Tuple[int, int] = (0, 0), alpha: float = .5, background: str = 'gray',
                 popup: bool = True, message: str = 'Saved successfully.', ok_title: str = 'Tips',
                 sleep_secs: float = 1.0, fill: str = 'white', outline: str = 'red'):
        """
        Easy Player printscreen window tool.
        
        Warning: available only on Windows system.
        
        :param save_path: Image save path.
        :param pos: Window position.
        :param alpha: Window transparency.
        :param background: Background color.
        :param popup: Whether to display information after successful screenshot.
        :param message: Display information after successful screenshot.
        :param ok_title: Title of the display information window after successful screenshot.
        :param sleep_secs: Waiting time after successful screenshot.
        :param fill: Fill color.
        :param outline: Outline color.
        """
        self._x, self._y = pos
        self._scale = 1
        
        self._save_path = save_path
        self._sleep_secs = sleep_secs
        
        self._popup = popup
        self._message = message
        self._ok_title = ok_title
        
        self._fill = fill
        self._outline = outline
        
        self._window = tk.Tk()
        self._window.attributes('-alpha', alpha)
        self._window.attributes('-fullscreen', True)
        self._window.attributes('-topmost', True)
        self._window.title('Print Screen')
        
        self._width, self._height = self._window.winfo_screenwidth(), self._window.winfo_screenheight()
        self._canvas = tk.Canvas(self._window, width=self._width, height=self._height, bg=background)
        
        self._window.bind('<Button-1>', self.click_left)
        self._window.bind('<ButtonRelease-1>', self.click_left)
        self._window.bind('<B1-Motion>', self.mouse_moving)
        self._window.bind('<Escape>', self.quit)
        
        user32 = ctypes.windll.user32
        gdi32 = ctypes.windll.gdi32
        dc = user32.GetDC(None)

        width_scale = gdi32.GetDeviceCaps(dc, 8)  # Width after resolution scaling
        width = gdi32.GetDeviceCaps(dc, 118)  # Original resolution width
        self._scale = width / width_scale
        
        self.image = None
        
        self._window.mainloop()
        
    def quit(self, _):
        """
        Quit this window.
        
        :param _: Tkinter event.
        :return: None
        """
        self._window.destroy()
        
    def click_left(self, event):
        """
        Callback function, when click left button.
        
        :param event: Tkinter event.
        :return: None
        """
        if event.state == 8:
            self._x, self._y = event.x, event.y
        elif event.state == 264:
            if event.x == self._x or event.y == self._y:
                return
            bbox = (self._scale * self._x + 2, self._scale * self._y + 2,
                    self._scale * event.x, self._scale * event.y)
            image = ImageGrab.grab(bbox)
            self.image = image
            image.save(self._save_path)
            if self._popup:
                showinfo(self._ok_title, self._message)
            time.sleep(self._sleep_secs)
            self._window.destroy()
            
    def mouse_moving(self, event):
        """
        Callback function, when mouse is moving.

        :param event: Tkinter event.
        :return: None
        """
        if event.x == self._x or event.y == self._y:
            return
        self._canvas.delete('rect')  # Update rectangle
        self._canvas.create_rectangle(self._x, self._y, event.x, event.y,
                                      fill=self._fill, outline=self._outline, tag='rect')
        self._canvas.pack()
        
    @property
    def pillow(self):
        """
        Get the PIL.Image.Image object of the screenshot image.
        
        :return: The PIL.Image.Image object of the screenshot image.
        """
        return self.image
        

def print_screen(save_path: str = 'grab.png', pos: Tuple[int, int] = (0, 0), alpha: float = .5, background: str = 'gray',
                 popup: bool = True, message: str = 'Saved successfully.', ok_title: str = 'Tips',
                 sleep_secs: float = 1.0, fill: str = 'white', outline: str = 'red'):
    """
    Create a Easy Player printscreen window tool and return it.
    
    Warning: available only on Windows system.
    
    :param save_path: Image save path.
    :param pos: Window position.
    :param alpha: Window transparency.
    :param background: Background color.
    :param popup: Whether to display information after successful screenshot.
    :param message: Display information after successful screenshot.
    :param ok_title: Title of the display information window after successful screenshot.
    :param sleep_secs: Waiting time after successful screenshot.
    :param fill: Fill color.
    :param outline: Outline color.
    :return: Easy Player printscreen window tool.
    """
    return _PrintScreenWindow(save_path, pos, alpha, background, popup, message, ok_title,
                              sleep_secs, fill, outline)
