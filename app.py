# flask app to serve a random file from a directory
from pydub import AudioSegment

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
        # convert ogg file to mp3
        ogg = AudioSegment.from_ogg(f)
        mp3 = ogg.export(format="mp3")
        return mp3.read()




if __name__ == "__main__":
    app.run()
