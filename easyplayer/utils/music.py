import pygame

try:
    from pydub import AudioSegment
except (ImportError, ModuleNotFoundError, AttributeError):
    from easyplayer.exceptions import EasyPlayerModuleError
    
    class _raise_error(object):
        @staticmethod
        def from_mp3(file_path: str):
            raise EasyPlayerModuleError('Please install ffmpeg and pydub')
    
    AudioSegment = _raise_error


def _mp3_to_wav(mp3_path: str, wav_path: str):
    song = AudioSegment.from_mp3(mp3_path)
    song.export(wav_path, format='wav')
    return wav_path


__all__ = ['Player', 'play_sound']


class Player(object):
    def __init__(self, sound: str, temp_wav: str = 'temp.wav'):
        if sound.lower().endswith('.mp3'):
            sound = _mp3_to_wav(sound, temp_wav)
        self._mixer = pygame.mixer
        self._mixer.init()
        self._mixer_load = self._mixer.Sound(sound)
        
    def play(self, loops: int = 0, max_time: int = 0, fade_ms: int = 0):
        self._mixer_load.play(loops, max_time, fade_ms)
        
    def fadeout(self, time: int):
        self._mixer_load.fadeout(time)
        
    def pause(self):
        self._mixer.pause()
        
    def unpause(self):
        self._mixer.unpause()
        
    @property
    def volume(self):
        return self._mixer_load.get_volume() * 100
        
    @volume.setter
    def volume(self, set_vol: int):
        self._mixer_load.set_volume(set_vol / 100)
        
    def stop(self):
        self._mixer_load.stop()
        
    def set_values(self, frequency: int = 44100, size: int = -16, channels: int = 2, buffer: int = 512):
        self._mixer.pre_init(frequency, size, channels, buffer)
        self._mixer.init(frequency, size, channels, buffer)
        

def play_sound(sound: str):
    Player(sound).play()
