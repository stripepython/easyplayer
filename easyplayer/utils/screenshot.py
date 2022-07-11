"""
Easy Player screenshot module.
"""

import pygame

from easyplayer.core.saver import queue
from easyplayer.exceptions import EasyPlayerSaverError


__all__ = ['Screenshot', 'save_screenshot']


class Screenshot(object):
    def __init__(self):
        """
        Easy Player screenshot tool.
        """
        if not queue:
            raise EasyPlayerSaverError('please created a game first')
        self._game = queue[-1]

    def save(self, save_path='screenshot.png'):
        """
        Save the screenshot.
        
        :param save_path: The save path of the screenshot.
        :return: None
        """
        pygame.image.save(self._game.screen, save_path)
        

def save_screenshot(save_path='screenshot.png'):
    """
    Save the screenshot.
    
    :param save_path: The save path of the screenshot.
    :return: Save path.
    """
    Screenshot().save(save_path)
    return save_path
