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
    static_path = os.path.join(app.root_path, "static")
    images = sorted(os.listdir(static_path))
    return render_template("index.html", images=images)


@app.route("/image/<filename>")
def image(filename):
    static_path = os.path.join(app.root_path, "static", filename)
    return send_file(static_path, mimetype="image/png")


@app.route("/circle", methods=["POST"])
def circle():
    tile_type = request.form.get("tile", "circle")

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


@app.route("/planet", methods=["POST"])
def planet():
    has_moon = request.form.get("moon", None) != None
    print(has_moon)

    colors = generate_random_colors(10)
    planet_color = choice(colors)
    
    img = Image.new("RGB", SIZE, color="white")
    draw = ImageDraw.Draw(img)

    planet_radius = randint(75, 150)
    c = Circle(512, 512, planet_radius)

    start = randint(0, 180)
    end = start + 180

    draw.pieslice(c.box(), start, end, fill=planet_color)

    ring_major = randint(400, 600)
    ring_minor = randint(30, 60)
    print(f"{planet_radius=}, {ring_major=}")

    r = Ellipse(512, 512, 190, 40)
    ring_angle = 180 - start
    for i in range(randint(5, 15)):
        img = ellipse_with_angle(img, r.x, r.y, ring_major + (i * 30),
        ring_minor + (i * 5), ring_angle, choice(colors))
    draw.pieslice(c.box(), end, start, fill=planet_color)

    # Move the moon closer to or further away from the planet
    distance_from_planet = randint(-50, 50) 

    # Offset the moon's position along the plane of rotation/planet's equator
    moon_plane_offset = randint(-30, 30)

    if has_moon:
        ring_radians = math.radians(ring_angle)
        side_of_planet = choice([start, end])
        moon_angle = math.radians(side_of_planet)
        distance = c.radius + distance_from_planet
        normal_angle = ring_radians + math.pi / 2

        moon = Circle(
            c.x + distance * math.cos(moon_angle) + moon_plane_offset * math.cos(normal_angle),
            c.y + distance * math.sin(moon_angle) + moon_plane_offset * math.sin(normal_angle),
            20,
            fill_color=choice(colors)
        )
        draw.ellipse(moon.box(), **moon.display_kwargs)
    return show_image(img)


if __name__ == '__main__':
    app.run(debug=True)
