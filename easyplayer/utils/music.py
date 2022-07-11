"""
Easy Player play music module.
"""

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


def _mp3_to_ogg(mp3_path: str, ogg_path: str):
    """
    Use pydub to convert MP3 to OGG.
    
    :param mp3_path: MP3 sound path.
    :param ogg_path: Save OGG file path.
    :return: Save OGG file path.
    """
    song = AudioSegment.from_mp3(mp3_path)
    song.export(ogg_path, format='ogg')
    return ogg_path


__all__ = ['Player', 'play_sound']


class Player(object):
    def __init__(self, sound: str, temp_ogg: str = 'temp.ogg'):
        """
        Easy Player music player.
        
        The Sound can be loaded from an OGG audio file or from an uncompressed WAV.
        
        When using MP3 format, ffmpeg running environment is required.
        
        :param sound: Sound path.
        :param temp_ogg: Temporary OGG sound file when using MP3 format.
        """
        if sound.lower().endswith('.mp3'):
            sound = _mp3_to_ogg(sound, temp_ogg)
        self._mixer = pygame.mixer
        self._mixer.init()
        self._mixer_load = self._mixer.Sound(sound)
        
    def play(self, loops: int = 0, max_time: int = 0, fade_ms: int = 0):
        """
        Play sound.
        
        :param loops: How many times the sample will be repeated after being played the first time.
        :param max_time: Used to stop playback after a given number of milliseconds.
        :param fade_ms: It'll make the sound start playing at 0 volume and fade up to full volume over the time given. The sample may end before the fade-in is complete.
        :return: None
        """
        self._mixer_load.play(loops, max_time, fade_ms)
        
    def fadeout(self, time: int):
        """
        Stop sound playback after fading out
        
        :param time: Fading out time.
        :return: None
        """
        self._mixer_load.fadeout(time)
        
    def pause(self):
        """
        Pause play sound.
        
        :return: None
        """
        self._mixer.pause()
        
    def unpause(self):
        """
        Unpause play sound.

        :return: None
        """
        self._mixer.unpause()
        
    @property
    def volume(self):
        return self._mixer_load.get_volume()
        
    @volume.setter
    def volume(self, set_vol: int):
        self._mixer_load.set_volume(set_vol)
        
    def stop(self):
        """
        Stop playing sound.
        
        :return: None
        """
        self._mixer_load.stop()
        
    def set_values(self, frequency: int = 44100, size: int = -16, channels: int = 2, buffer: int = 512):
        """
        Set the values of this player.
        
        :param frequency: The frequency of this player.
        :param size: How many bits are used for each audio sample.
        :param channels: 1 for mono and 2 for stereo.
        :param buffer: The number of internal samples used in the sound mixer. The default value should work for most cases.
        :return: None
        """
        self._mixer.pre_init(frequency, size, channels, buffer)
        self._mixer.init(frequency, size, channels, buffer)
        

def play_sound(sound: str):
    """
    Play sound.
    
    The Sound can be loaded from an OGG audio file or from an uncompressed WAV.
    
    When using MP3 format, ffmpeg running environment is required.
    
    :param sound: Sound file path.
    :return: None
    """
    Player(sound).play()
