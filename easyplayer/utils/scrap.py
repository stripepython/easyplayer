from typing import AnyStr

from pygame import constants

try:
    from pygame import scrap
except (ModuleNotFoundError, ImportError, AttributeError):
    from easyplayer.exceptions import EasyPlayerModuleError
    
    class _raise_error(object):
        @staticmethod
        def init():
            raise EasyPlayerModuleError('This version of pygame does not support scrap') from None

    scrap = _raise_error
  
__all__ = ['scrap_types', 'Scrap']

    
class _ScrapTypes(object):
    ppm = constants.SCRAP_PPM
    pbm = constants.SCRAP_PBM
    bmp = constants.SCRAP_BMP
    txt = constants.SCRAP_TEXT
 
    
scrap_types = _ScrapTypes


class Scrap(object):
    def __init__(self):
        self._pg_scrap = scrap
        self._pg_scrap.init()
        
    def __getitem__(self, item: str):
        return self.get(item)
    
    def __setitem__(self, key: str, value: AnyStr):
        self.put(key, value)
        
    def __contains__(self, item: str):
        return self.contains(item)
        
    def get(self, scrap_type: str):
        return self._pg_scrap.get(scrap_type)
    
    def put(self, scrap_type: str, data: AnyStr):
        self._pg_scrap.put(scrap_type, data)
        
    def contains(self, scrap_type: str):
        return self._pg_scrap.contains(scrap_type)
