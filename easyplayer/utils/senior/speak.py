"""
Easy Player speaking robot module.
"""

from typing import Optional, Any
from dataclasses import dataclass

import pyttsx3
from pyttsx3.voice import Voice

__all__ = ['speak', 'SpeakEngine']


def speak(text: str):
    """
    Read a text.
    
    :param text: The text.
    :return: None
    """
    pyttsx3.speak(text)
    

@dataclass()
class SpeakOptions(object):
    id: str
    name: str
    languages: list
    gender: None
    name: None
    
    def __init__(self, voice: Voice):
        """
        The options of the speaking robot.

        :param voice: pyttsx3.voice.Voice object.
        """
        self.voice = voice
        
        self.id = voice.id
        self.name = voice.name
        self.age = voice.age
        self.gender = voice.gender
        self.languages = voice.languages
    

class SpeakEngine(object):
    def __init__(self, driver_name: Optional[str] = None, debug: bool = False):
        """
        Easy Player speaking robot.
        
        :param driver_name: Name of the platform specific driver to use. If
        None, selects the default driver for the operating system.
        :param debug: Debugging output enabled or not.
        """
        self.engine = pyttsx3.init(driver_name, debug)
        
    def __getitem__(self, item: str):
        return self.engine.getProperty(item)
    
    def __setitem__(self, key: str, value: Any):
        self.engine.setProperty(key, value)
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.say()
        
    @property
    def rate(self):
        return self.engine.getProperty('rate')
    
    @rate.setter
    def rate(self, set_rate: int):
        self.engine.setProperty('rate', set_rate)

    @property
    def volume(self):
        return self.engine.getProperty('volume')

    @volume.setter
    def volume(self, set_volume: int):
        self.engine.setProperty('volume', set_volume)

    @property
    def option_id(self):
        return self.engine.getProperty('voice')

    @option_id.setter
    def option_id(self, set_option_id: str):
        self.engine.setProperty('voice', set_option_id)
        
    @property
    def options(self):
        return [SpeakOptions(v) for v in self.engine.getProperty('voices')]
        
    def speak(self, text: str):
        """
        Read a text.
        
        You need to execute SpeakEngine.say function after this function to make sound

        :param text: The text.
        :return: None
        """
        self.engine.say(text)
        
    def say(self):
        """
        Start reading. This function is required to make sound.
        
        Such as:
        
        >>> import easyplayer as ep
        >>> engine = ep.SpeakEngine()
        >>> engine.speak('Easy Player')
        >>> engine.speak('Life is short, I use Python.')
        >>> engine.say()
        
        Or:
        
        >>> import easyplayer as ep
        >>> with ep.SpeakEngine() as engine:
        >>>     engine.speak('Easy Player')
        >>>     engine.speak('Life is short, I use Python.')
        
        :return: None
        """
        self.engine.runAndWait()
        
    def stop(self):
        """
        Stop speaking.
        
        :return: None
        """
        self.engine.stop()
        
    def save_to(self, text: str, file_path: str = 'temp.mp3'):
        """
        Save the reading sound to a file.
        
        You need ffmpeg running environment.
        
        :param text: The text.
        :param file_path: Save sound file's path.
        :return: None
        """
        self.engine.save_to_file(text, file_path)
        
    @property
    def busy(self):
        return self.engine.isBusy()
