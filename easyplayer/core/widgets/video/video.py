from typing import Optional, Tuple

import pygame

from easyplayer.core.saver import queue
from easyplayer.exceptions import EasyPlayerSaverError
from easyplayer.core.widgets.video.clip import video2images, get_fps

__all__ = ['Video']
    

class Video(object):
    def __init__(self, video: str, size: Optional[Tuple[int, int]] = None,
                 progress_bar: bool = True, set_fps: bool = True):
        """
        Easy Player video widget.
        Provides simple video playback.
        
        Implementation method:
        1. Decomposing video into picture sets, read all into memory (Memory errors may occur when the video is too large).
        2. Play frame by frame (May lead to a large number of resource losses.)
        
        Warning: this is the test function, it is unstable!
        
        :param video: Video path, support AVI (in uncompressed format), AVI(MPEG1), AVI(DIVX), AVI(XVID), AVI(ffdshow MPEG-4),
        AVI(WMV9), AVI(VP6), MKV, OGG, MP4
        :param size: Video player size.
        :param progress_bar: Whether to display terminal progress bar.
        :param set_fps: Whether to automatically set window's FPS as video's FPS.
        """
        if not queue:
            raise EasyPlayerSaverError('please created a game first')
        self._game = queue[-1]
        self._screen = self._game.screen
        
        if set_fps:
            fps = get_fps(video)
            self._game.set_fps(fps)
        
        self.images = video2images(video, progress_bar)
        if size:
            self.images = [pygame.transform.scale(i, size) for i in self.images]
        self.index = 0
        self.loops = 0
        
        self.x, self.y = 0, 0
        
    @property
    def pos(self):
        return self.x, self.y
    
    @pos.setter
    def pos(self, set_pos: Tuple[int, int]):
        self.x, self.y = set_pos
        
    def next(self):
        """
        Play next frame.
        
        :return: None
        """
        self.index += 1
        
    def update(self):
        """
        Update and display pictures.
        
        :return: None
        """
        if 0 <= self.index < len(self.images):
            image = self.images[self.index]
            self._screen.blit(image, (self.x, self.y))
        else:
            self.loops += 1
            self.index = 0
            
    def show(self):
        """
        Play next frame.
        Update and display pictures.
        
        :return: Whether the second time is not played.
        """
        self.update()
        self.next()
        return self.loops == 0
    
    def pack(self):
        """
        Pack this video object.

        :return: None
        """
        self._game.add_sprite(self)
