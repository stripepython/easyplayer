"""
Easy Player camera widget.
Like a video player.

Supports Linux (V4L2) and Windows (MSMF) cameras natively.
"""

from typing import Tuple, List, Union, Dict, Optional

import pygame
import pygame.camera

from easyplayer.core.saver import queue
from easyplayer.exceptions import EasyPlayerSaverError, EasyPlayerCameraError

__all__ = ['ColorModes', 'Camera']


class _ColorModes(object):
    """
    Support color modes.
    """
    RGB = 'RGB'
    HSV = 'HSV'
    YUV = 'YUV'
   
    
ColorModes = _ColorModes


class Camera(object):
    def __init__(self, device: Optional[str] = None,
                 size: Union[Tuple[int, int], List[int]] = (640, 360),
                 color_mode: str = ColorModes.RGB,
                 start: bool = True):
        """
        Easy Player camera widget.
        Like a video player.

        Supports Linux (V4L2) and Windows (MSMF) cameras natively.
        
        :param device: Camera name. If the value is blank, it will be selected automatically.
        :param size: Camera size.
        :param color_mode: Camera color mode. Support RGB, HSV and YUV.
        :param start: Auto start shooting.
        """
        if not queue:
            raise EasyPlayerSaverError('please create a game first')
        self._game = queue[-1]
        self._screen = self._game.screen
        self._camera = pygame.camera
        self._last = None
        self._init()
        if not self._camera.list_cameras():
            raise EasyPlayerCameraError('No photographic hardware available')
        if device is None:
            device = self._camera.list_cameras()[0]
        
        self.camera = self._camera.Camera(device, size, color_mode)
        
        self.x, self.y = 0, 0
        self.update = self.show
        
        if start:
            self.start()
            
    def __getitem__(self, item):
        return self.controls[item]
    
    def __setitem__(self, key, value):
        dct = self.controls
        dct[key] = value
        self.controls = dct
        
    def __missing__(self, key):
        raise EasyPlayerCameraError(f'{key} not found') from None
        
    def _init(self):
        self._camera.init(None)
        if not self._camera.list_cameras():
            raise EasyPlayerCameraError('No cameras available')
        
    def start(self):
        """
        Start shooting.
        
        :return: None
        """
        self.camera.start()
        
    def stop(self):
        """
        Stop shooting.

        :return: None
        """
        self.camera.stop()

    @property
    def pos(self):
        return self.x, self.y

    @pos.setter
    def pos(self, set_pos: Tuple[int, int]):
        self.x, self.y = set_pos
        
    @property
    def size(self):
        return self.camera.get_size()
    
    @property
    def controls(self):
        hflip, vfilp, brightness = self.camera.get_controls()
        return {'hfilp': hflip, 'vfilp': vfilp, 'brightness': brightness}
    
    @controls.setter
    def controls(self, values: Dict[str, Union[bool, int]]):
        self.camera.set_controls(**values)
        
    def flip_horizontally(self):
        """
        Flip horizontally.
        
        :return: None
        """
        self.camera.set_controls(hflip=True)
        
    def flip_vertically(self):
        """
        Flip vertically.

        :return: None
        """
        self.camera.set_controls(vflip=True)
        
    def set_brightness(self, brightness: int):
        """
        Set brightness of this camera.

        :param brightness: Brightness.
        :return: None
        """
        self.camera.set_controls(brightness=brightness)
        
    def save_image(self, save_path: str = 'camera.jpg'):
        """
        Save picture of current frame.
        
        :param save_path: Image path.
        :return: Save path.
        """
        raw = self.camera.get_raw()
        with open(save_path, 'wb') as img:
            img.write(raw)
        return save_path
        
    def show(self, raise_for_stopped: bool = False):
        """
        Show and update this camera object.
        
        :param raise_for_stopped: Whether an exception is thrown when stopping photography.
        :raise: EasyPlayerCameraError
        :return: None
        """
        try:
            image = self.camera.get_image()
            self._last = image
        except pygame.error as err:
            if raise_for_stopped:
                err = EasyPlayerCameraError(str(err))
                raise err from None
            image = self._last
        if image is not None:
            self._screen.blit(image, (self.x, self.y))
        
    def pack(self):
        """
        Pack this camera object.
        
        :return: None
        """
        self._game.add_sprite(self)
