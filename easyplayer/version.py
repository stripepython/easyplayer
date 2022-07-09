"""
Easy Player's version manager.
You can use it for compatibility checks.

Such as:

>>> import easyplayer as ep
>>> if ep.version.major != 0:
>>>     raise SystemExit('Version wrong.')
"""

from typing import Tuple

__all__ = ['version']


class _Version(tuple):
    def __init__(self, *nums: Tuple[int]):
        self.major, self.minor, self.micro = nums
    
    def __new__(cls, *args):
        return tuple.__new__(cls, args)
    
    def __str__(self):
        return '{}.{}.{}'.format(*self)
    
    
version = _Version(0, 2, 1)
