from flask import Flask, render_template, send_file
import os

from v1.api import v1
from v2.api import v2

app = Flask(__name__)
app.register_blueprint(v1)
app.register_blueprint(v2)


@app.route("/")
def index():
    api_versions = ["v1", "v2"]
    return render_template(
        "index.html",
        api_versions=api_versions)


if __name__ == '__main__':
    app.run(debug=True)
