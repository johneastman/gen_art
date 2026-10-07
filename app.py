from flask import Flask, render_template, request, send_file
from io import BytesIO
import math
import os

from PIL import Image, ImageDraw
from random import randint, choice
from shapes import Circle, Ellipse
from util import ellipse_with_angle, generate_random_colors, intersect

app = Flask(__name__)

SIZE = (1024, 1024)
WIDTH, HEIGHT = SIZE
BORDER_WIDTH = 2


def show_image(img: Image):
    img_io = BytesIO()
    img.save(img_io, 'PNG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype="image/png")


@app.route("/")
def index():
    images = sorted(os.listdir("static"))
    return render_template("index.html", images=images)


@app.route("/image/<filename>")
def image(filename):
    return render_template("image.html", filename=filename)


@app.route("/circle")
def circle():
    tile_type = request.args.get("tile", "circle")

    # outer-most circle for which other circles reside in
    main = Circle(WIDTH // 2, HEIGHT // 2, 490)

    colors = generate_random_colors(10)

    circles = []

    for _ in range(10000):
        radius = randint(8, 32)

        x, y = Circle.generate(main.x, main.y, main.radius - radius)

        circle_kwargs = {**{
            "fill_color": choice(colors),
            **({"border_color": "white", "border_width": BORDER_WIDTH} 
            if tile_type == "square" else {})
        }}
        c = Circle(x, y, radius, **circle_kwargs)

        if not intersect(circles, c):
            circles.append(c)

    img = Image.new("RGB", SIZE, color="white")
    draw = ImageDraw.Draw(img)

    for c in circles:
        shape_box = c.box()
        match tile_type:
            case "circle":
                draw.ellipse(shape_box, **c.display_kwargs)
            case "square":
                draw.rectangle(shape_box, **c.display_kwargs)
            case _:
                draw.ellipse(shape_box, **c.display_kwargs)

    return show_image(img)


@app.route("/planet")
def planet():
    colors = generate_random_colors(10)
    body_color = choice(colors)

    img = Image.new("RGB", SIZE, color="white")
    draw = ImageDraw.Draw(img)

    planet_radius = randint(75, 150)
    c = Circle(512, 512, planet_radius)

    start = randint(0, 180)
    end = start + 180

    draw.pieslice(c.box(), start, end, fill=body_color)

    ring_major = randint(400, 600)
    ring_minor = randint(30, 60)
    print(f"{planet_radius=}, {ring_major=}")

    r = Ellipse(512, 512, 190, 40)
    for i in range(randint(5, 15)):
        img = ellipse_with_angle(img, r.x, r.y, ring_major + (i * 30), ring_minor + (i * 5), 180 - start, choice(colors))
    draw.pieslice(c.box(), end, start, fill=body_color)

    # Moon potential
    #
    # PADDING = 100
    # p1 = Circle(
    #     ((c.radius + PADDING) * math.cos(start * math.pi / 180)) + c.x,
    #     ((c.radius + PADDING) * math.sin(start * math.pi / 180)) + c.y,
    #     20,
    #     border_color="green"
    # )
    # draw.ellipse(p1.box(), **p1.display_kwargs)

    # p2 = Circle(
    #     ((c.radius + PADDING) * math.cos(end * math.pi / 180)) + c.x,
    #     ((c.radius + PADDING) * math.sin(end * math.pi / 180)) + c.y,
    #     20,
    #     fill_color="green"
    # )
    # draw.ellipse(p2.box(), **p2.display_kwargs)
    return show_image(img)


if __name__ == '__main__':
    app.run(debug=True)
