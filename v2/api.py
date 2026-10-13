from flask import Blueprint, redirect, render_template, request, send_file, url_for
from io import BytesIO
import os
from random import choice

from PIL import Image, ImageDraw

from .shapes import Shape
from util import generate_random_colors, show_image

API_VERSION = "v2"
v2 = Blueprint(API_VERSION, __name__, url_prefix=f"/api/{API_VERSION}")


@v2.route("/")
def index():
    return render_template(
        os.path.join(API_VERSION, "index.html"),
        api_version=API_VERSION)


@v2.route("/tile", methods=["POST"])
def tile():
    tile_type = request.form.get("tile", "circle")
    canvas_shape = request.form.get("shape", "circle")
    canvas_layout = request.form.get("layout", "random")

    colors = generate_random_colors(10)

    CELL_SIZE = 64
    CANVAS_SIZE = (1024, 1024)
    CANVAS_WIDTH, CANVAS_HEIGHT = CANVAS_SIZE

    # The last and bottom row of pixels are cutoff. Adding 1 to the width
    # and height accounts for this and ensures the whole image is visible
    img = Image.new("RGB", (CANVAS_WIDTH + 1, CANVAS_HEIGHT + 1), color="white")
    draw = ImageDraw.Draw(img)

    shapes = []
    for x in range(0, CANVAS_WIDTH, CELL_SIZE):
        for y in range(0, CANVAS_HEIGHT, CELL_SIZE):
            shape = Shape(
                x, y, CELL_SIZE, 
                fill_color=choice(colors),
                border_color="black"
            )
            shapes.append(shape)

    for shape in shapes:
        draw.rectangle(shape.box(), **shape.display_kwargs)

    return show_image(img)
