"""A script for generative art

TODO: https://stackoverflow.com/questions/30608035/plot-circular-gradients-using-pil-in-python
"""
from PIL import Image, ImageDraw
import numpy as np
from shapes import *  # shapes.py


def intersect(circles, circle):
    for c in circles:
        if c.intersect(circle, padding=2):
            return True
    return False


def random_pixels(filename):
    SIZE = (1080, 1920, 3)
    arr = np.random.randint(0, 255, size=SIZE)

    img = Image.fromarray(arr.astype("uint8"))
    img.show()
    img.save(filename)


if __name__ == "__main__":
    SIZE = (1024, 1024)
    WIDTH, HEIGHT = SIZE
    BORDER_WIDTH = 2

    # outer-most circle for which other circles reside in
    main = Circle(WIDTH // 2, HEIGHT // 2, 490)

    colors = util.generate_random_colors(10)

    circles = []

    for _ in range(10000):
        radius = random.randint(8, 32)

        x, y = Circle.generate(main.x, main.y, main.radius - radius)

        c = Circle(x, y, radius, fill_color=random.choice(colors))
        if not intersect(circles, c):
            circles.append(c)

    img = Image.new("RGB", SIZE, color="white")
    draw = ImageDraw.Draw(img)

    for c in circles:
        draw.ellipse(c.box(), **c.display_kwargs)

    img.show()
