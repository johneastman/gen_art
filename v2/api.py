from flask import Blueprint, redirect, render_template, request, send_file, url_for
from io import BytesIO
import os
from random import choice

from PIL import Image, ImageDraw

from .csp import CSP
from .shapes import Shape
from util import generate_random_colors, show_image

API_VERSION = "v2"
v2 = Blueprint(API_VERSION, __name__, url_prefix=f"/api/{API_VERSION}")


@v2.route("/")
def index():
    return render_template(
        os.path.join(API_VERSION, "index.html"),
        api_version=API_VERSION)


def backtrack(assignments, neighbors, colors):
    # Have all cells been colored?
    if len(assignments) == len(neighbors):
        return True

    # Find a cell that hasn't been colored yet
    coordinate = next(
        cell for cell in neighbors
        if cell not in assignments
    )

    # Try each available color
    for color in colors:
        if is_valid(coordinate, color, assignments, neighbors):
            # Make the assignment
            assignments[coordinate] = color

            # Recursively color the remaining cells
            if backtrack(assignments, neighbors, colors):
                return True

            # Dead end! Undo the assignment and try another color
            del assignments[coordinate]

    # No color worked for this cell
    return False


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

    # Generate coordinates and neighbors
    neighbors = {}
    for x in range(0, CANVAS_WIDTH, CELL_SIZE):
        for y in range(0, CANVAS_HEIGHT, CELL_SIZE):
            # Neighboring cells' coordinates
            neighbors[(x, y)] = []
            if x - CELL_SIZE >= 0:
                neighbors[(x, y)].append((x - CELL_SIZE, y))
            if x + CELL_SIZE < CANVAS_WIDTH:
                neighbors[(x, y)].append((x + CELL_SIZE, y))
            if y - CELL_SIZE >= 0:
                neighbors[(x, y)].append((x, y - CELL_SIZE))
            if y + CELL_SIZE < CANVAS_HEIGHT:
                neighbors[(x, y)].append((x, y + CELL_SIZE))

    # Find a solution that meets the constraints
    csp = CSP(neighbors, colors)
    if csp.backtrack():
        for (x, y), color in csp.assignments.items():
            shape = Shape(
                x, y,
                CELL_SIZE,
                fill_color=color,
                border_color="black"
            )
            draw.rectangle(shape.box(), **shape.display_kwargs)
        return show_image(img)
    else:
        return {"error": "No Solution"}
