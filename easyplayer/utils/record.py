"""
Easy Player record sound module.

You need to install pyaudio and its running environment.

Note: pyaudio is not installed by default!

Such as:

>>> import easyplayer as ep
>>> with ep.recorder('test.wav') as r:
>>>     r.record_time(15)  # record 15s
"""

from typing import Callable
import wave

try:
    from pyaudio import PyAudio, paInt8, paInt16, paInt24, paInt32
except (ModuleNotFoundError, ImportError, AttributeError):
    from easyplayer.exceptions import EasyPlayerModuleError
    
    class _raise_error(object):
        def __init__(self, *args, **kwargs):
            raise EasyPlayerModuleError('Please install pyaudio')
        
    PyAudio = _raise_error
    paInt8 = paInt16 = paInt24 = paInt32 = 0


_FORMAT_DICT = {
    8: paInt8,
    16: paInt16,
    24: paInt24,
    32: paInt32,
}  # Define paInt format dict


__all__ = ['recorder']


class _Recorder(object):
    def __init__(self, save_path: str = 'record.wav', chunk: int = 1024,
                 channels: int = 1, rate: int = 44100, format_: int = 16):
        """
        Easy Player sound recorder.
        
        You need to install pyaudio and its running environment.

        Note: pyaudio is not installed by default!
        
        :param save_path: Sound file save path.
        :param chunk: Specifies the number of frames per buffer.
        :param channels: Number of channels.
        :param rate: Sampling rate.
        :param format_: Sampling size and format.
        """
        self._p = PyAudio()
        format_ = _FORMAT_DICT.get(format_, paInt16)
        
        self._stream = self._p.open(
            format=format_,
            channels=channels,
            rate=rate,
            input=True,
            frames_per_buffer=chunk
        )  # Create stream
        
        self._chunk = chunk
        self._rate = rate
        self._channels = channels
        self._format = format_
        self.set_file(save_path)
        
        self._running = True
        
    def save(self):
        self._stream.stop_stream()
        self._stream.close()
        self._p.terminate()
        self._file.close()
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()
        
    def record(self):
        """
        Record one frame of audio.
        
        :return: None
        """
        data = self._stream.read(self._chunk)
        self._file.writeframes(data)
            
    def record_time(self, seconds: float):
        """
        Record audio in a given number of seconds.
        
        :param seconds: Number of seconds to record audio.
        :return: None
        """
        n = int(self._rate / self._chunk * seconds)
        for i in range(n):
            self.record()
            
    def set_file(self, save_path: str):
        """
        Reset save path.
        
        :param save_path: Sound file save path.
        :return: None
        """
        self._file = wave.open(save_path, 'wb')
        self._file.setnchannels(self._channels)
        self._file.setsampwidth(self._p.get_sample_size(self._format))
        self._file.setframerate(self._rate)
        

def recorder(save_path: str = 'record.wav', chunk: int = 1024,
             channels: int = 1, rate: int = 44100, format_: int = 16):
    """
    Create a new sound recorder and return it.

    You need to install pyaudio and its running environment.

    Note: pyaudio is not installed by default!

    :param save_path: Sound file save path.
    :param chunk: Specifies the number of frames per buffer.
    :param channels: Number of channels.
    :param rate: Sampling rate.
    :param format_: Sampling size and format.
    :return: The new sound recorder
    """
    return _Recorder(save_path, chunk, channels, rate, format_)
