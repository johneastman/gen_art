from PIL import Image, ImageDraw
from shapes import Circle, Ellipse
import math
from random import randint, choice
import util  # util.py


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


if __name__ == "__main__":
    SIZE = (1024, 1024)

    colors = util.generate_random_colors(10)
    body_color = choice(colors)

    img = Image.new("RGB", SIZE, color="white")
    draw = ImageDraw.Draw(img)

    planet_radius = randint(75, 150)
    c = Circle(512, 512, planet_radius)

    start = randint(0, 180)
    end = start + 180

    PADDING = 100

    draw.pieslice(c.box(), start, end, fill=body_color)

    ring_major = randint(400, 600)
    ring_minor = randint(30, 60)

    # planet_radius=121, ring_major=200
    print(f"{planet_radius=}, {ring_major=}")

    r = Ellipse(512, 512, 190, 40)
    for i in range(randint(5, 15)):
        img = ellipse_with_angle(img, r.x, r.y, ring_major + (i * 30), ring_minor + (i * 5), 180 - start, choice(colors))
    draw.pieslice(c.box(), end, start, fill=body_color)

    '''
    p1 = Circle(
        ((c.radius + PADDING) * math.cos(start * math.pi / 180)) + c.x,
        ((c.radius + PADDING) * math.sin(start * math.pi / 180)) + c.y,
        20,
        border_color="green"
    )
    draw.ellipse(p1.box(), **p1.display_kwargs)

    p2 = Circle(
        ((c.radius + PADDING) * math.cos(end * math.pi / 180)) + c.x,
        ((c.radius + PADDING) * math.sin(end * math.pi / 180)) + c.y,
        20,
        fill_color="green"
    )
    draw.ellipse(p2.box(), **p2.display_kwargs)
    '''
    img.show()
