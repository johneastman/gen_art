import math
import random

import util  # util.py


class Shape:
    """Base class for all Shape objects."""
    def __init__(self, x, y, width, height, fill_color=None, border_color=None, border_width=1):
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.display_kwargs = {
            "fill": fill_color,
            "outline": border_color,
            "width": border_width
        }

    def box(self):
        """Return the coordinates of the box that is used to draw the shape. Shapes are placed on the canvas from their
        center point, which is to say that (x, y) is the center of all shapes.

        :return:
        """
        return self.x - self.width, self.y - self.height, self.x + self.width, self.y + self.height


class Rectangle(Shape):
    def __init__(self, x, y, width, height, **kwargs):
        super().__init__(x, y, width, height, **kwargs)


class Ellipse(Rectangle):
    def __init__(self, x, y, width, height, **kwargs):
        super().__init__(x, y, width, height, **kwargs)

    @property
    def semi_major_axis(self):
        return max(self.width, self.height)

    @property
    def semi_minor_axis(self):
        return min(self.width, self.height)


class Square(Rectangle):
    def __init__(self, x, y, width, **kwargs):
        super().__init__(x, y, width, width, **kwargs)
    
    def generate(self, width):
        """Generate a random x-y pair within the bounds of this square."""
        max_width = max(self.width, width)
        min_width = min(self.width, width)

        max_height = max(self.height, width)
        min_height = min(self.height, width)

        x = random.randint(self.x - ((max_width - min_width) // 2), self.x + ((max_width - min_width) // 2))
        y = random.randint(self.y - ((max_height - min_height) // 2), self.y + ((max_height - min_height) // 2))
        return x, y


class Circle(Shape):

    def __init__(self, x, y, radius, **kwargs):
        super().__init__(x, y, radius, radius, **kwargs)
        self.radius = radius

    def intersect(self, other, padding=0):
        """Check if two circles intersect.

        :param other: The circle being compared to this one
        :param padding: Adds additional values to distance. Used when the two circles should not touch.
        :return: true if both circles intersect; false otherwise
        """
        return util.distance(other.x, self.x, other.y, self.y) - padding <= self.radius + other.radius

    def generate(self, radius):
        """Generate a random x-y pair within the bounds of this circle.

        Source:
        https://www.mathworks.com/matlabcentral/answers/360361-how-to-generate-uniform-random-points-with-in-a-circle
        """
        max_radius = max(self.radius, radius)
        min_radius = min(self.radius, radius)

        # Square root ensures a more even distribution of points within the circle.
        # Subtracting the new circle's radius from this circle's radius ensures no
        # circles fall outside the bounds of this circle.
        r = (max_radius - min_radius) * math.sqrt(random.random())

        f = random.random() # random fraction/percentage of circle (between 0 and 1)
        x, y = util.point_on_circumference(
            self.x, self.y, r, f
        )
        return x, y
