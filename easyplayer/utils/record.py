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
}


__all__ = ['recorder']


class _Recorder(object):
    def __init__(self, save_path: str = 'record.wav', chunk: int = 1024,
                 channels: int = 1, rate: int = 44100, format_: int = 16):
        self._p = PyAudio()
        format_ = _FORMAT_DICT.get(format_, paInt16)
        
        self._stream = self._p.open(
            format=format_,
            channels=channels,
            rate=rate,
            input=True,
            frames_per_buffer=chunk
        )
        
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
        
    def start(self, func: Callable, *args, **kwargs):
        while func(*args, **kwargs):
            data = self._stream.read(self._chunk)
            self._file.writeframes(data)
            
    def record_time(self, seconds: float):
        n = int(self._rate / self._chunk * seconds)
        for i in range(n):
            data = self._stream.read(self._chunk)
            self._file.writeframes(data)
            
    def set_file(self, save_path: str):
        self._file = wave.open(save_path, 'wb')
        self._file.setnchannels(self._channels)
        self._file.setsampwidth(self._p.get_sample_size(self._format))
        self._file.setframerate(self._rate)
        

def recorder(save_path: str = 'record.wav', chunk: int = 1024,
             channels: int = 1, rate: int = 44100, format_: int = 16):
    return _Recorder(save_path, chunk, channels, rate, format_)
