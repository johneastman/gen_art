import math
import random
import string

from PIL import Image, ImageDraw


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


def ellipse_with_angle(im, x, y, major, minor, angle, color):
    """Source: https://stackoverflow.com/a/44159636

    :param im:
    :param x:
    :param y:
    :param major:
    :param minor:
    :param angle:
    :param color:
    :return:
    """
    # take an existing image and plot an ellipse centered at (x,y) with a
    # defined angle of rotation and major and minor axes.
    # center the image so that (x,y) is at the center of the ellipse
    x -= int(major / 2)
    y -= int(major / 2)

    # create a new image in which to draw the ellipse
    im_ellipse = Image.new('RGBA', (major, major), (255, 255, 255, 0))
    draw_ellipse = ImageDraw.Draw(im_ellipse, "RGBA")

    # draw the ellipse
    ellipse_box = (0, int(major / 2 - minor / 2), major, int(major / 2 - minor / 2) + minor)
    draw_ellipse.ellipse(ellipse_box, outline=color, width=3)

    # rotate the new image
    rotated = im_ellipse.rotate(angle)
    rx, ry = rotated.size

    # paste it into the existing image and return the result
    im.paste(rotated, (x, y, x + rx, y + ry), mask=rotated)
    return im



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


def generate_random_colors(n):
    """Return a list of randomly-generated colors in hexadecimal format

    :param n: number of colors to generate
    :return: list of colors
    """
    return [f"#{''.join(random.choices(string.hexdigits, k=6))}" for _ in range(n)]


def intersect(circles, circle):
    for c in circles:
        if c.intersect(circle, padding=2):
            return True
    return False


def is_outside_anchor(anchor_points, exclusion_radius, point):
    px, py = point
    for x, y in anchor_points:
        dx = px - x;
        dy = py - y;
        if dx ** 2 + dy ** 2 < exclusion_radius ** 2:
            return False
    return True
