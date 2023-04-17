# flask app to serve a random file from a directory
from flask import Flask, render_template
import os
import random
import string

app = Flask(__name__, template_folder="templates")


@app.route("/a")
def random_file():
    """
    Returns a random .ogg file from a directory inducting subdirectories
    """
    path = "data/"
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if ".ogg" in file:
                files.append(os.path.join(r, file))
    with open(random.choice(files), "rb") as f:
        return f.read()


@app.route("/")
def index():
    """
    Returns the index.html file
    """
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
