"""
Easy Player coordinate tools module
"""

from typing import Union, Iterable, Optional, Tuple, List

import dataclasses
from pygame.math import Vector2

from easyplayer.core.saver import queue
from easyplayer.exceptions import EasyPlayerSaverError, EasyPlayerCoordinateError

__all__ = ['LTCoordinate', 'LBCoordinate', 'NormalCoordinate', 'CoordinateType', 'parse_coordinate']


def _parse(pos: Union[complex, Iterable[Union[int, float]], Union[int, float]] = 0,
           y: Optional[Union[int, float]] = None):
    """
    Parse a coordinate.
    
    :param pos: Coordinate.
    :param y: If the pos parameter represents X coordinate, this parameter represents y coordinate.
    :return: Coordinate Tuple.
    """
    if isinstance(pos, Iterable):
        return tuple(pos)
    if isinstance(pos, (int, float)):
        return pos, y
    if isinstance(pos, complex):
        return pos.real, pos.imag
    

def _get_screen_rect():
    """
    Get the screen rect of this game.
    
    :raise: EasyPlayerSaverError
    :return: Screen rect
    """
    if not queue:
        raise EasyPlayerSaverError('please create a game first')
    return queue[-1].screen.get_rect()


@dataclasses.dataclass()
class LTCoordinate(object):
    x: Union[int, float] = 0
    y: Union[int, float] = 0
    
    def __init__(self, pos: Union[complex, Iterable[Union[int, float]], Union[int, float]] = 0,
                 y: Optional[Union[int, float]] = None):
        """
        Create coordinates with the upper left corner of the screen as the origin,
        the x-axis right, and the y-axis down.
        
        You can call it in many ways:
        
        >>> import easyplayer as ep
        >>> a = ep.LTCoordinate((100, 100))
        >>> b = ep.LTCoordinate(100, 100)
        >>> c = ep.LTCoordinate(100+100j)
        >>> d = ep.LTCoordinate(complex(100, 100))
        >>> e = ep.LTCoordinate([100, 100])
        >>> f = ep.LTCoordinate(ep.vectors.Vector2(100, 100))
        >>> assert a == b == c == d == e == f
        
        :param pos: Coordinate.
        :param y: If the pos parameter represents X coordinate,
        this parameter represents y coordinate.
        """
        self.x, self.y = _parse(pos, y)
        self._inx = 0
        
    def __complex__(self):
        return self.x + self.y * 1j
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._inx == 0:
            self._inx += 1
            return self.x
        if self._inx == 1:
            self._inx += 1
            return self.y
        raise StopIteration
    
    @property
    def origin(self):
        return 0, 0
    
    def to_tuple(self):
        """
        Convert to coordinates available to Easy Player.
        
        :return: Coordinates available to Easy Player.
        """
        return self.x, self.y
    
    def to_left_bottom(self):
        """
        Convert to LBCoordinate.
        
        :return: LBCoordinate.
        """
        screen_rect = _get_screen_rect()
        return LBCoordinate(self.x, screen_rect.height - self.y)
    
    def to_normal(self):
        """
        Convert to NormalCoordinate.

        :return: NormalCoordinate.
        """
        screen_rect = _get_screen_rect()
        cx, cy = screen_rect.center
        return NormalCoordinate(self.x - cx, -self.y + cy)
    
    to_lb = to_left_bottom
    to_nl = to_normal
    to_te = to_tuple


@dataclasses.dataclass()
class LBCoordinate(object):
    x: Union[int, float] = 0
    y: Union[int, float] = 0
    
    def __init__(self, pos: Union[complex, Iterable[Union[int, float]], Union[int, float]] = 0,
                 y: Optional[Union[int, float]] = None):
        """
        Create coordinates with the lower left corner of the screen as the origin,
        X-axis right, Y-axis up
        
        API is the same as LTCoordinate.
        
        :param pos: Coordinate.
        :param y: If the pos parameter represents X coordinate,
        this parameter represents y coordinate.
        """
        self.x, self.y = _parse(pos, y)
        self._inx = 0
        
    def __complex__(self):
        return self.x + self.y * 1j

    def __iter__(self):
        return self

    def __next__(self):
        if self._inx == 0:
            self._inx += 1
            return self.x
        if self._inx == 1:
            self._inx += 1
            return self.y
        raise StopIteration
    
    @property
    def origin(self):
        screen_rect = _get_screen_rect()
        return 0, screen_rect.height
    
    def to_tuple(self):
        """
        Convert to coordinates available to Easy Player.

        :return: Coordinates available to Easy Player.
        """
        return self.to_left_top().to_tuple()
    
    def to_left_top(self):
        """
        Convert to LTCoordinate.

        :return: LTCoordinate.
        
        :return: LTCoordinate.
        """
        screen_rect = _get_screen_rect()
        return LTCoordinate(self.x, screen_rect.height - self.y)
    
    def to_normal(self):
        """
        Convert to NormalCoordinate.

        :return: NormalCoordinate.
        """
        screen_rect = _get_screen_rect()
        cx, cy = screen_rect.center
        return NormalCoordinate(self.x - cx, self.y - cy)
    
    to_lt = to_left_top
    to_nl = to_normal
    to_te = to_tuple
    

@dataclasses.dataclass()
class NormalCoordinate(object):
    x: Union[int, float] = 0
    y: Union[int, float] = 0
    
    def __init__(self, pos: Union[complex, Iterable[Union[int, float]], Union[int, float]] = 0,
                 y: Optional[Union[int, float]] = None):
        self.x, self.y = _parse(pos, y)
        self._inx = 0
        
    def __complex__(self):
        return self.x + self.y * 1j
        
    def __iter__(self):
        return self

    def __next__(self):
        if self._inx == 0:
            self._inx += 1
            return self.x
        if self._inx == 1:
            self._inx += 1
            return self.y
        raise StopIteration
    
    @property
    def origin(self):
        screen_rect = _get_screen_rect()
        return screen_rect.center
    
    def to_tuple(self):
        return self.to_left_top().to_tuple()
    
    def to_left_top(self):
        screen_rect = _get_screen_rect()
        cx, cy = screen_rect.center
        return LTCoordinate(cx + self.x, cy - self.y)
    
    def to_left_bottom(self):
        screen_rect = _get_screen_rect()
        cx, cy = screen_rect.center
        return LBCoordinate(cx + self.x, cy + self.y)
    
    to_lt = to_left_top
    to_lb = to_left_bottom
    to_te = to_tuple
    

CoordinateType = Union[
    LTCoordinate, LBCoordinate, NormalCoordinate,
    Tuple[Union[int, float], Union[int, float]],
    List[Union[int, float]],
    complex, Vector2
]

def parse_coordinate(coordinate: CoordinateType):
    if isinstance(coordinate, (LTCoordinate, tuple, list, Vector2)):
        res = tuple(coordinate)
        if len(res) != 2:
            raise EasyPlayerCoordinateError('Not a coordinate')
        return res
    if isinstance(coordinate, (LBCoordinate, NormalCoordinate)):
        return tuple(coordinate.to_left_top())
    if isinstance(coordinate, complex):
        return coordinate.real, coordinate.imag
    raise EasyPlayerCoordinateError('Not a coordinate')
