import math
import random
import string


def distance(x1, x2, y1, y2):
    """Returns the distance between two points.

    Point #1 -> (x1, y1)
    Point #2 -> (x2, y2)

    :param x1: x value for Point #1
    :param x2: x value for Point #2
    :param y1: y value for Point #1
    :param y2: y value for Point #2
    :return: Distance between Point #1 and Point #2
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def line_between_circles(c1, c2):
    """Draws a line between two circles.

    The line starts at the center of the first circle and goes through the center of the second circle to that circle's
    edge. An example of what this function does can be found here: https://stackoverflow.com/q/61769184

    :param c1: first circle
    :param c2: second circle
    :return: returns a 4-tuple containing the coordinates of the two points for the line between both circles. The
    returned values are (c1.x, c1.y, c2 edge through c2.x, c2 edge through c2.y)
    """
    a = c2.x - c1.x
    b = c2.y - c1.y
    d = distance(c1.x, c2.x, c1.y, c2.y)

    return c1.x, c1.y, c2.x + c2.radius * a / d, c2.y + c2.radius * b / d


def random_point_in_circle(r1):
    """Generate a random coordinate within a circle.

    Source for this function can be found here: https://stackoverflow.com/a/30564123

    :param r1: radius of circle
    :return: (x, y) coordinate of random point within the circle of radius r1
    """
    p = 2 * math.pi * random.random()
    r = r1 * math.sqrt(random.random())

    x = (math.cos(p) * r) + r1
    y = (math.sin(p) * r) + r1
    return x, y


def generate_random_colors(n):
    """Return a list of randomly-generated colors in hexadecimal format

    :param n: number of colors to generate
    :return: list of colors
    """
    return [f"#{''.join(random.choices(string.hexdigits, k=6))}" for _ in range(n)]
