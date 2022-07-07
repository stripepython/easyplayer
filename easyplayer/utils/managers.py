"""
Easy Player managers tools module.
"""

import copy
from typing import Any, Tuple

from pygame.sprite import Group, Sprite, groupcollide, spritecollide

from easyplayer.core.saver import queue
from easyplayer.exceptions import EasyPlayerSaverError, EasyPlayerOnlyReadError

__all__ = ['VariableManager', 'CloneManager']


class VariableManager(object):
    def __init__(self, **var):
        """
        Easy Player global variables manager.
        
        :param var: Variables.
        """
        self._dict = var
        self._only_read = set()
        
    def __str__(self):
        return ';'.join(f'{k}={v}' for k, v in self._dict.items())
    
    def __copy__(self):
        """
        Copy a same variable manager.
        
        :return: The same variable manager.
        """
        return VariableManager(**self._dict.copy())
    
    def __deepcopy__(self, memodict=None):
        """
        Deepcopy a same variable manager.

        :return: The same variable manager.
        """
        return VariableManager(**copy.deepcopy(self._dict))
    
    copy = __copy__
    deepcopy = __deepcopy__
    
    def __getitem__(self, item: Any):
        try:
            return self._dict[item]
        except KeyError:
            raise KeyError(str(item)) from None
    
    def __setitem__(self, key: Any, value: Any):
        if key in self._only_read:
            raise EasyPlayerOnlyReadError(f'{key} is only-read.')
        self._dict[key] = value
        
    def __delitem__(self, key: Any):
        if key in self._only_read:
            raise EasyPlayerOnlyReadError(f'{key} is only-read.')
        del self._dict[key]
    
    def __len__(self):
        return len(self._dict)
    
    def __iter__(self):
        return self._dict.items()
    
    def only_read(self, var_name: str):
        """
        Set a variable only-read.
        
        :param var_name: Variable name.
        :return: None
        """
        self._only_read.add(var_name)
        
    def de_only_read(self, var_name: str):
        """
        Cancel a variable only-read.

        :param var_name: Variable name.
        :return: None
        """
        if var_name in self._only_read:
            self._only_read.remove(var_name)
            
    def create(self, class_: type):
        """
        Create an object based on what is stored in the variable.
        
        :param class_: Object class.
        :return: The object.
        """
        return class_(**self._dict)
    
    
class CloneManager(object):
    def __init__(self, *sprites: Tuple[Sprite]):
        """
        Easy Player clone manager.
        
        :param sprites: Clones.
        """
        if not queue:
            raise EasyPlayerSaverError('please create a game first')
        self._game = queue[-1]
        self._screen = self._game.screen
        self._sprites = Group(*sprites)
        
    def __copy__(self):
        """
        Copy a same clone manager and return it.
        
        :return: The same clone manager.
        """
        return CloneManager(*self._sprites.sprites())
    
    copy = __copy__
    
    def __contains__(self, item: Sprite):
        return self.has(item)
    
    def __iter__(self):
        yield from self._sprites.sprites()
        
    def __bool__(self):
        return len(self._sprites.sprites()) != 0
        
    def add(self, sprite: Sprite):
        self._sprites.add(sprite)
        
    def remove(self, sprite: Sprite):
        self._sprites.remove(sprite)
        
    def has(self, sprite: Sprite):
        self._sprites.has(sprite)
        
    def show(self, *args, **kwargs):
        self._sprites.draw(self._screen)
        self._sprites.update(*args, **kwargs)
    
    def clear(self):
        self._sprites.empty()
    
    @property
    def group(self):
        return self._sprites
    
    def collide_clones(self, other, kill_self: bool = False, kill_other: bool = False):
        return groupcollide(self._sprites, other.group, kill_self, kill_other)
    
    def collide_sprites(self, sprite: Sprite, kill_it: bool = False):
        return spritecollide(sprite, self._sprites, kill_it)
    
    def collide_other(self, other, kill_self: bool = False, kill_other: bool = False):
        if isinstance(other, CloneManager):
            return self.collide_clones(other, kill_self, kill_other)
        return self.collide_sprites(other, kill_other)
    