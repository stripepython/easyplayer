"""
Easy Player's version manager.
You can use it for compatibility checks.

Such as:

>>> import easyplayer as ep
>>> if ep.version.major != 0:
>>>     raise SystemExit('Version wrong.')
"""
from dataclasses import dataclass

__all__ = ['version', 'major', 'minor', 'micro', 'vernum', 'verstr']


@dataclass()
class _Version(tuple):
    major: int
    minor: int
    micro: int
    
    def get_tuple(self):
        return self.major, self.minor, self.micro
    
    def get_string(self):
        return f'{self.major}.{self.minor}.{self.micro}'
    
    
version = _Version(0, 1, 2)
major = version.major
minor = version.minor
micro = version.micro
vernum = version.get_tuple()
verstr = version.get_string()
