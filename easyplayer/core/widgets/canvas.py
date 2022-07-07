"""
Easy Player graphic tools.
"""

from typing import Tuple, Union, List, Sequence

import pygame
from pygame import draw
from pygame import gfxdraw

from easyplayer.core.saver import queue
from easyplayer.exceptions import EasyPlayerSaverError, EasyPlayerCanvasError
from easyplayer.utils.color import ColorType

__all__ = ['Canvas', 'Pen']

PointType = Union[List[int], Tuple[int, int], pygame.math.Vector2]


class Canvas(object):
    def __init__(self, size: PointType = (100, 100), bgcolor: ColorType = (0, 0, 0)):
        """
        Easy Player canvas object.
        
        :param size: Canvas size.
        :param bgcolor: Canvas background color.
        """
        if not queue:
            raise EasyPlayerSaverError('please create a game first')
        self._game = queue[-1]
        self._screen = self._game.screen
        self.width, self.height = size
        self.rect = pygame.rect.Rect(0, 0, self.width, self.height)
        self.bgcolor = bgcolor
        
    def show(self):
        """
        Show this canvas object.
        
        :return: None
        """
        draw.rect(self._screen, self.bgcolor, self.rect)
    
    @property
    def pos(self):
        return self.rect.x, self.rect.y
    
    @pos.setter
    def pos(self, set_pos: Tuple[int, int]):
        self.rect.x, self.rect.y = set_pos

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, set_x: int):
        self.rect.x = set_x

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, set_y: int):
        self.rect.y = set_y
        
    def init_pen(self):
        """
        Get the pen of this canvas.
        
        :return: The pen of this canvas.
        """
        return Pen(self)
    
    def pack(self):
        """
        Pack this canvas object.
        
        :return: None
        """
        self._game.add_sprite(self)
    
    
class Pen(object):
    def __init__(self, canvas: Canvas, color: ColorType = (255, 255, 255)):
        """
        Easy Player pen object.
        
        :param canvas: Father canvas.
        :param color: Pen color.
        """
        if not queue:
            raise EasyPlayerSaverError('please created a game first')
        self._game = queue[-1]
        self._screen = self._game.screen
        
        self.canvas = canvas
        self.color = color
        
    def set_color(self, color: ColorType):
        """
        Set color of this pen.
        
        :param color: Pen color.
        :return: None
        """
        self.color = color
       
    def circle(self, center: PointType, radius: int = 30, fill: bool = True, width: int = 1):
        """
        Draw a circle(jagged).
        
        :param center: The centre of circle coordinates.
        :param radius: The radius length of this circle.
        :param fill: Whether to fill.
        :param width: Border width.
        :return: None
        """
        if fill:
            width = 0
        draw.circle(self._screen, self.color, center, radius, width=width)
        
    def rect(self, pos: PointType, size: PointType, fill: bool = True, width: int = 1):
        """
        Draw a rectangle.

        :param pos: Coordinates of upper left corner of rectangle.
        :param size: Rectangle size.
        :param fill: Whether to fill.
        :param width: Border width.
        :return: None
        """
        if fill:
            width = 0
        rect = pygame.rect.Rect(pos, size)
        draw.rect(self._screen, self.color, rect, width=width)
        
    rectangle = rect
        
    def line(self, start_pos: PointType, end_pos: PointType,
             width: int = 1, antialias: bool = True):
        """
        Draw a line.

        :param start_pos: Start position.
        :param end_pos: End position.
        :param width: Border width.
        :param antialias: Whether antialias.
        :return: None
        """
        func = draw.aaline if antialias else draw.line
        func(self._screen, self.color, start_pos, end_pos, width)

    def polygon(self, points: List[PointType], fill: bool = True, width: int = 1):
        """
        Draw a polygon
        
        :param points: Polygon vertex coordinate list.
        :param fill: Whether to fill.
        :param width: Border width.
        :return: None
        """
        if len(points) < 3:
            raise EasyPlayerCanvasError('The number of polygon sides must be greater than 2')
        if fill:
            width = 0
        draw.polygon(self._screen, self.color, points, width=width)
        
    def ellipse(self, pos: PointType, size: PointType, fill: bool = True, width: int = 1):
        """
        Draw a ellipse.
        
        :param pos: Coordinates of upper left corner of rectangle to which the ellipse belongs.
        :param size: Rectangle to which the ellipse belongs size.
        :param fill: Whether to fill.
        :param width: Border width.
        :return: None
        """
        if fill:
            width = 0
        rect = pygame.rect.Rect(pos, size)
        draw.ellipse(self._screen, self.color, rect, width=width)
        
    def triangle(self, point1: PointType, point2: PointType, point3: PointType, fill: bool = True):
        """
        Draw a triangle.
        
        :param point1: First vertex coordinate of triangle.
        :param point2: Second vertex coordinate of triangle
        :param point3: Third vertex coordinate of triangle
        :param fill: Whether to fill.
        :return: None
        """
        x1, y1 = point1
        x2, y2 = point2
        x3, y3 = point3
        if fill:
            gfxdraw.filled_trigon(self._screen, x1, y1, x2, y2, x3, y3, self.color)
        else:
            gfxdraw.trigon(self._screen, x1, y1, x2, y2, x3, y3, self.color)
    
    def arc(self, point: PointType, radius: int, start_angel: int, stop_angel: int):
        """
        Draw a arc.
        
        :param point: Coordinate of the center of the arc.
        :param radius: Radius of the arc.
        :param start_angel: Start angle in degrees.
        :param stop_angel: Stop angle in degrees.
        :return: None
        """
        x, y = point
        gfxdraw.arc(self._screen, x, y, radius, start_angel, stop_angel, self.color)
        
    def pie(self, point: PointType, radius: int, start_angel: int, stop_angel: int):
        """
        Draw a pie.

        :param point: Coordinate of the center of the pie.
        :param radius: Radius of the pie.
        :param start_angel: Start angle in degrees.
        :param stop_angel: Stop angle in degrees.
        :return: None
        """
        x, y = point
        gfxdraw.pie(self._screen, x, y, radius, start_angel, stop_angel, self.color)
        
    def bezier(self, points: Sequence[PointType], steps: int = 10):
        """
        Draw a Bezier curve.
        
        :param points: A sequence of 3 or more (x, y) coordinates used to form a curve, where each coordinate in the sequence must be a PointType.
        :param steps: Number of steps for the interpolation, the minimum is 2.
        :return: None
        """
        gfxdraw.bezier(self._screen, points, steps, self.color)
