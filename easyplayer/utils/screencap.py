"""
Easy Player screencap module.

Such as:

>>> import easyplayer as ep
>>> window = ep.Window('Test', fps=5)
>>> bar = ep.Bar()
>>> bar.pack()
>>> screencap = ep.Screencap()
>>> @window.when_draw
>>> def when_draw():
>>>     bar.set_proportion(ep.random.random())
>>>     screencap.record()
>>> window.show()
"""

from typing import Optional, Tuple

import cv2

from easyplayer.utils.screenshot import save_screenshot
from easyplayer.core.saver import queue
from easyplayer.exceptions import EasyPlayerSaverError

__all__ = ['ScreencapEncodings', 'Screencap']


class _Encodings(object):
    """
    Collected all of opencv encodings.
    """
    I420 = 'I420'
    XVID = 'XVID'
    PIM1 = 'PIM1'
    THEO = 'THEO'
    FLV1 = 'FLV1'
    AVC1 = 'ACV1'
    DIV3 = 'DIV3'
    DIVX = 'DIVX'
    MP42 = 'MP42'
    MJPG = 'MJPG'
    U263 = 'U263'
    I263 = 'I263'
    

ScreencapEncodings = _Encodings


class Screencap(object):
    def __init__(self):
        """
        Easy Player screencap tool.
        """
        if not queue:
            raise EasyPlayerSaverError('please created a game first')
        self._game = queue[-1]
        self._images = []
        self._start = True
        
    def start(self):
        """
        Start recording.
        
        :return: None
        """
        self._start = True
        
    def stop(self):
        """
        Stop recording.

        :return: None
        """
        self._start = False
        
    def record(self, temp_file: str = 'temp.png'):
        """
        Record one frame.
        
        :param temp_file: Temporary picture file path.
        :return: None
        """
        save_screenshot(temp_file)
        array = cv2.imread(temp_file)
        self._images.append(array)
        
    def save(self, video_path: str = 'screencap.avi', encoding: str = ScreencapEncodings.I420,
             fps: Optional[float] = None, size: Optional[Tuple[int, int]] = None):
        """
        Save video file.
        
        :param video_path: Video file path.
        :param encoding: OpenCV encoding.
        :param fps: The FPS of the video. Default value is window's FPS.
        :param size: The size of the video.
        :return: None
        """
        if not fps:
            fps = self._game.fps
        if not size:
            size = self._game.size
        fourcc = cv2.VideoWriter_fourcc(*encoding)
        writer = cv2.VideoWriter(video_path, fourcc, fps, size)
        
        for img in self._images:
            frame = cv2.resize(img, size)
            writer.write(frame)
        
        writer.release()
        cv2.destroyAllWindows()
        
    @property
    def images_array(self):
        """
        Get images' arrays.
        
        :return: The generator of images' arrays.
        """
        yield from self._images
