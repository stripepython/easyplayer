"""
Easy Player saver
"""

from random import choice

__all__ = ['queue', 'SpriteQueue']

queue = []  # 窗口队列，用于存档

class SpriteQueue(object):
    def __init__(self):
        """
        Easy Player sprite layer displays the queue.
        
        Note: the element at the end of the queue is placed at the top level (opposite to the layer order).
        """
        self.queue = []
        
    def __str__(self):
        return f'SpriteQueue()'
    
    def __getitem__(self, item):
        return self.queue[item]
    
    def __setitem__(self, key, value):
        self.queue[key] = value
        
    def append(self, item):
        """
        Put a sprite at the end of the queue (at the top)
        
        :param item: A sprite.
        :return: None
        """
        self.queue.append(item)
        
    def remove(self, item):
        """
        If the sprite is in the game queue, delete the sprite (only once).
        
        Note: this function first deletes the sprite at the bottom of the layer.
        
        :param item: A sprite.
        :return: None
        """
        if item in self.queue:
            self.queue.remove(item)
            
    def clear(self):
        """
        Reset the sprite queue and remove all elements.
        
        :return: None
        """
        self.queue.clear()
        
    def random(self):
        """
        Gets a random sprite in the queue.
        
        :return: A random sprite.
        """
        return choice(self.queue)
    
    def swap(self, sprite1, sprite2):
        """
        If both sprite 1 and sprite 2 exist in the queue, the positions of the two sprites are exchanged.
        
        Note: This function gives priority to moving the role at the bottom of the layer.
        
        :param sprite1: Sprite 1.
        :param sprite2: Sprite 2.
        :return: None
        """
        if (sprite1 in self.queue) and (sprite2 in self.queue):
            a, b = self.queue.index(sprite1), self.queue.index(sprite2)
            if a != b:
                self.queue[a], self.queue[b] = self.queue[b], self.queue[a]
                
    def move(self, sprite, index: int):
        """
        If the sprite is in the queue, move the sprite to the specified location.
        
        Note: This function gives priority to moving the role at the bottom of the layer.
        
        :param sprite: The sprite.
        :param index: Sprite index.
        :return: None
        """
        if sprite in self.queue:
            self.queue.insert(index, sprite)
            self.remove(sprite)
            
    def move_first(self, sprite):
        """
        If the sprite is in the queue, move the sprite to the top level.
        
        Note: This function gives priority to moving the role at the bottom of the layer.

        :param sprite: A sprite.
        :return: None
        """
        self.move(sprite, -1)
        
    def move_last(self, sprite):
        """
        If the sprite is in the queue, move the sprite to the bottom level.
        
        Note: This function gives priority to moving the role at the bottom of the layer.

        :param sprite: A sprite.
        :return: None
        """
        self.move(sprite, 0)
