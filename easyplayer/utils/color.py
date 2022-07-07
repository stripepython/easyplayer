"""
Easy Player color tool.
"""

from typing import Union, Tuple, List

import pygame

__all__ = ['Color', 'ColorType']


def _count_hue(h: int, u: int, e: int):
    """
    A math function.
    
    :param h: H.
    :param u: U.
    :param e: E.
    :return: HUE.
    """
    e += (
        1 if e < 0
        else -1 if e > 1
        else 0
    )
    if (6 * e) < 1:
        return h + (u - h) * 6 * e
    if (2 * e) < 1:
        return u
    if (3 * e) < 2:
        return h + (u - h) * (2 / 3 - e) * 6
    return h


class Color(pygame.color.Color):
    def __init__(self, *args, **kwargs):
        """
        Easy Player color tool class.
        
        Like this:
        
        >>> from easyplayer import Color
        >>> red = Color(255, 0, 0)
        
        :param args: Arguments of pygame.color.Color.
        :param kwargs: Keyword arguments of pygame.color.Color.
        """
        super().__init__(*args, **kwargs)
        
    @staticmethod
    def from_hex(string: Union[int, str], alpha: int = 255):
        """
        Create a RGB color tool from HEX color.
        
        :param string: HEX string.
        :param alpha: Alpha value.
        :return: The RGB color.
        """
        if isinstance(string, str):
            string = string.replace('#', '')
            num = int(string, base=16)
        else:
            num = int(string)
        rgba = (
            (num >> 16) & 0xFF,
            (num >> 8) & 0xFF,
            num & 0xFF,
            alpha
        )
        return Color(*rgba)
    
    @staticmethod
    def from_hsv(h: int, s: int, v: int, alpha: int = 255):
        """
        Create a RGB color tool from HSV color.

        :param h: H.
        :param s: S.
        :param v: V.
        :param alpha: Alpha value.
        :return: The RGB color.
        """
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c

        choices = [
            (c, x, 0), (x, c, 0), (0, c, x),
            (0, x, c), (x, 0, c), (c, 0, x)
        ]  # Define cases
        lower, upper = 0, 60
        r1, g1, b1 = 0, 0, 0
        for n in choices:
            if lower < h < upper:
                r1, g1, b1 = n
            lower += 60
            upper += 60

        r = (r1 + m) * 255
        g = (g1 + m) * 255
        b = (b1 + m) * 255
        
        return Color(r, g, b, alpha)

    @staticmethod
    def from_hsl(h: int, s: int, L: int, alpha: int = 255):
        """
        Create a RGB color tool from HSL color.

        :param h: H.
        :param s: S.
        :param L: L.
        :param alpha: Alpha value.
        :return: The RGB color.
        """
        if s == 0:
            r = g = b = L * 255
        else:
            y = L * 6 if L < .5 else (L + s) - (s * L)
            x = 2 * L - y
            r = 255 * _count_hue(x, y, h + 1 / 3)
            g = 255 * _count_hue(x, y, h)
            b = 255 * _count_hue(x, y, h - 1 / 3)
        return Color(r, g, b, alpha)
    
    @staticmethod
    def from_cmyk(c: int, m: int, y: int, k: int, alpha: int = 255):
        """
        Create a RGB color tool from CMYK color.

        :param c: C.
        :param m: M.
        :param y: Y.
        :param k: K.
        :param alpha: Alpha value.
        :return: The RGB color.
        """
        rk = 255 * (1 - k)
        rgba = (
            (1 - c) * rk,
            (1 - m) * rk,
            (1 - y) * rk,
            alpha
        )
        return Color(*rgba)
    
    @staticmethod
    def from_yuv(y: int, u: int, v: int, alpha: int = 255):
        """
        Create a RGB color tool from HSV color.

        :param y: Y.
        :param u: U.
        :param v: V.
        :param alpha: Alpha value.
        :return: The RGB color.
        """
        rgba = (
            y + 1.4075 * (v - 128),
            y - .3455 * (u - 128) - .7169 * (v - 128),
            y + 1.7790 * (u - 128),
            alpha
        )
        return Color(*rgba)
    
    
ColorType = Union[pygame.Color, Tuple[int, int, int], Tuple[int, int, int, int], List[int], Color]
