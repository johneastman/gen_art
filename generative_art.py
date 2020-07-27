"""A script for generative art

TODO: https://stackoverflow.com/questions/30608035/plot-circular-gradients-using-pil-in-python
"""
# import numpy as np
from PIL import Image, ImageDraw
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
    def generate(r):
        x, y = util.random_point_in_circle(r)
        x = int(x + (WIDTH - r * 2) / 2)
        y = int(y + (HEIGHT - r * 2) / 2)

        return x, y


def save_image(filename, img_arr):
    img = Image.fromarray(img_arr.astype("uint8"))
    img.show()
    # img.save(filename)


def intersect(circles, circle):
    for c in circles:
        if c.intersect(circle, padding=2):
            return True
    return False


if __name__ == "__main__":
    # SIZE = (1080, 1920, 3)
    # arr = np.random.randint(0, 255, size=SIZE)
    # save_image("", arr)

    SIZE = (1024, 1024)
    WIDTH, HEIGHT = SIZE
    BORDER_WIDTH = 2

    colors = util.generate_random_colors(10)

    # 2, 16 -> 512
    # 4, 32 -> 1024

    # outer-most circle for which other circles reside in
    main = Circle(WIDTH // 2, HEIGHT // 2, 490, border_color="red", border_width=BORDER_WIDTH)

    circles = []
    for _ in range(10000):
        radius = random.randint(8, 32)

        x, y = Circle.generate(main.radius - radius)

        # If the generated circle is NOT within the bounds of the outer-most circle, generate a new circle until one is
        # created that meets those requirements.
        # while d + radius >= main.radius:
        #     x, y, d = generate(main, radius)

        # if d + radius < main.radius:  #
        c = Circle(x, y, radius, fill_color=random.choice(colors))
        if not intersect(circles, c):
            circles.append(c)

    img = Image.new("RGB", SIZE, color="white")
    draw = ImageDraw.Draw(img)

    for c in circles:
        draw.ellipse(c.box(), **c.display_kwargs)
        # draw.line(util.line_between_circles(main, c), fill="black")

        # d = distance(main.x, c.x + c.r, main.y, c.y + c.r)
        # draw.text((c.x, c.y), f"{int(d)=}\n{c.r=}\n{main.r=}", fill="black")

    img.show()
