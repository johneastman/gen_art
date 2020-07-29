import math
import random

import util  # util.py


class Shape:
    """Base class for all Shape objects."""
    def __init__(self, x, y, fill_color=None, border_color=None, border_width=1):
        self.x = x
        self.y = y

        self.display_kwargs = {
            "fill": fill_color,
            "outline": border_color,
            "width": border_width
        }


class Rectangle(Shape):

    def __init__(self, x, y, width, height, **kwargs):
        super().__init__(x, y, **kwargs)
        self.width = width
        self.height = height


class Square(Rectangle):

    def __init__(self, x, y, width, **kwargs):
        super().__init__(x, y, width, width, **kwargs)


class Circle(Shape):

    def __init__(self, x, y, radius, **kwargs):
        super().__init__(x, y, **kwargs)
        self.radius = radius

    def box(self):
        return self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius

    def intersect(self, other, padding=0):
        """Check if two circles intersect.

        :param other: The circle being compared to this one
        :param padding: Adds additional values to distance. Used when the two circles should not touch.
        :return: true if both circles intersect; false otherwise
        """
        return util.distance(other.x, self.x, other.y, self.y) - padding <= self.radius + other.radius

    @staticmethod
    def generate(x0, y0, radius):
        """Generate an xy coordinate pair within the bounds of a given circle at position (x0, y0) and with a radius

        Source:
        https://www.mathworks.com/matlabcentral/answers/360361-how-to-generate-uniform-random-points-with-in-a-circle

        :param x0: x position of reference circle
        :param y0: y position of reference circle
        :param radius: radius of reference circle
        :return: random coordinates within reference circle
        """
        t = 2 * math.pi * random.random()
        r = radius * math.sqrt(random.random())
        x = x0 + r * math.cos(t)
        y = y0 + r * math.sin(t)
        return x, y
