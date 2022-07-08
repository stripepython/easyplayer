"""
Easy Player managers tools module.
"""

import copy
from typing import Any, Tuple, List

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
        
    def __bool__(self):
        return len(self._sprites.sprites()) != 0
        
    def add(self, sprite: Sprite):
        """
        Add a sprite.
        
        :param sprite: The sprite.
        :return: None
        """
        self._sprites.add(sprite)
        
    def remove(self, sprite: Sprite):
        """
        Remove a sprite.
        
        Delete the sprite at the top first.

        :param sprite: The sprite.
        :return: None
        """
        self._sprites.remove(sprite)
        
    def has(self, *sprites: List[Sprite]):
        """
        Returns True if the given sprite or sprites are contained in the group.
        
        :param sprites: Given sprite or sprites.
        :return: Sprite or sprites in this manager.
        """
        return self._sprites.has(*sprites)
        
    def show(self, *args, **kwargs):
        """
        Show this all sprites in this manager.
        
        :return: None
        """
        self._sprites.draw(self._screen)
        self._sprites.update()
    
    def clear(self):
        """
        Clear this manager.
        
        :return: None
        """
        self._sprites.empty()
    
    @property
    def group(self):
        return self._sprites
    
    def collide_clones(self, other, kill_self: bool = False, kill_other: bool = False):
        """
        Find sprites that collide with another manager in this manager.
        
        :param other: Other manager.
        :param kill_self: Delete the collision sprite in this manager.
        :param kill_other: Delete the collision sprite in other manager.
        :return: A dictionary of all sprites in this manager that collide.
        """
        return groupcollide(self._sprites, other.group, kill_self, kill_other)
    
    def collide_sprites(self, sprite: Sprite, kill_it: bool = False):
        """
        Find sprites that collide with another sprite in this manager.

        :param sprite: Other sprite.
        :param kill_it: Delete other sprite.
        :return: A list containing all Sprites in a manager that intersect with another sprite.
        """
        return spritecollide(sprite, self._sprites, kill_it)
    
    def collide_other(self, other, kill_self: bool = False, kill_other: bool = False):
        """
        Determine the collision event of this manager.
        
        When the other parameter is another manager, it calls the collide_clones function.
        When the other parameter is another sprite, it calls the collide_sprites function.
        
        :param other: Other.
        :param kill_self: Delete the collision sprite in this manager.
        :param kill_other: Delete other sprite.
        :return: collide_clones' return val or collide_sprites' return value.
        """
        if isinstance(other, CloneManager):
            return self.collide_clones(other, kill_self, kill_other)
        return self.collide_sprites(other, kill_other)
    