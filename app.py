# flask app to serve a random file from a directory
import base64

from flask import Flask, render_template
import os
import random
import string

app = Flask(__name__, template_folder="templates")


@app.route("/audio")
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
        # convert file to base64 string
        data = f.read()
        data = base64.b64encode(data)
        data = data.decode("utf-8")
        return data


if __name__ == "__main__":
    app.run()
