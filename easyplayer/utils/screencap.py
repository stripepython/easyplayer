from typing import Optional, Tuple

import cv2

from easyplayer.utils.screenshot import save_screenshot
from easyplayer.core.saver import queue
from easyplayer.exceptions import EasyPlayerSaverError

__all__ = ['ScreencapEncodings', 'Screencap']


class _Encodings(object):
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
        if not queue:
            raise EasyPlayerSaverError('please created a game first')
        self._game = queue[-1]
        self._images = []
        self._start = True
        
    def start(self):
        self._start = True
        
    def stop(self):
        self._start = False
        
    def record(self, temp_file: str = 'temp.png'):
        save_screenshot(temp_file)
        array = cv2.imread(temp_file)
        self._images.append(array)
        
    def save(self, video_path: str = 'screencap.avi', encoding: str = ScreencapEncodings.I420,
             fps: Optional[float] = None, size: Optional[Tuple[int, int]] = None):
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
        yield from self._images
