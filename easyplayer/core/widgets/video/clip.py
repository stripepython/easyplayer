"""
This is tool module for playing video.

Need numpy, opencv-python and tqdm.
"""

import numpy as np
import pygame

from easyplayer.exceptions import EasyPlayerModuleError

try:
    import cv2
except ImportError:
    class _raise_error(object):
        @staticmethod
        def VideoCapture(*args, **kwargs):
            raise EasyPlayerModuleError('Please install opencv-python')
        
    cv2 = _raise_error
    
try:
    import tqdm
except ImportError:
    class _raise_error(object):
        @staticmethod
        def tqdm(*args, **kwargs):
            raise EasyPlayerModuleError('Please install tqdm')
    
    tqdm = _raise_error
    
    
__all__ = ['video2images', 'get_fps']
    
    
def video2images(video_path: str, progress_bar: bool = True):
    """
    Decomposing video into picture sets.
    Save to pygame.Surface object list.
    Memory errors may occur when the video is too large.
    
    :param video_path: Video path.
    :param progress_bar: Whether to display terminal progress bar.
    :raise: MemoryError
    :return: pygame.Surface object list.
    """
    cap = cv2.VideoCapture(video_path)
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    bar = tqdm.tqdm(total=int(frames)) if progress_bar else None  # Create tqdm to show progress bar
    res = []
    while cap.isOpened():
        ret, frame = cap.read()
        if frame is not None:
            frame = np.fliplr(np.fliplr(cv2.transpose(frame)))   # Mirror horizontally twice after flipping
            surface = pygame.surfarray.make_surface(frame)
            res.append(surface)
        if progress_bar:
            bar.update()
        if not ret:
            break
    cap.release()  # Release video
    cv2.destroyAllWindows()
    return res
    

def get_fps(video_path: str):
    """
    Get a video's FPS.
    
    :param video_path: Video path.
    :return: This video's FPS.
    """
    cap = cv2.VideoCapture(video_path)
    return int(cap.get(cv2.CAP_PROP_FPS))
