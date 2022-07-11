"""
Easy Player timer module.
"""
import time

import pygame

__all__ = ['Timer', 'sleep']


def sleep(seconds: int):
    """
    Delay execution for a given number of seconds.
    
    :param seconds: The given number of seconds.
    :return: None
    """
    pygame.time.delay(int(seconds * 1000))


class Timer(object):
    def __init__(self):
        """
        Easy Player timer tool.
        """
        self._start_time = time.time()
        
    def __str__(self):
        return 'Timer()'
    
    def __int__(self):
        return int(self.time)
    
    def __float__(self):
        return self.time
    
    @property
    def time(self):
        """
        Current timer time.
        """
        return time.time() - self._start_time
    
    def zero(self):
        """
        Timer zeroing.
        
        :return: None
        """
        self._start_time = time.time()
        
    def get(self, digits: int = 2):
        """
        Get current timer time and make rounding treatment.
        
        :param digits: Digits precision after the decimal point.
        :return: Timer time after rounding.
        """
        return round(self.time, digits)
