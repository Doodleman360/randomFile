# flask app to serve a random file from a directory
from pydub import AudioSegment

from flask import Flask, render_template, request, send_file
import os
import random
import string

app = Flask(__name__, template_folder="templates")


@app.route("/audio.mp3")
def random_file():
    """
    Returns a random .mp3 file from a directory inducting subdirectories
    """
    directory = request.args.get('directory', default='data', type=str)
    path = "data/"
    if directory == "julien":
        path = "julien/"
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if ".mp3" in file:
                files.append(os.path.join(r, file))
    return send_file(random.choice(files), mimetype="audio/mp3", as_attachment=True)


def convertFiles():
    """
    Converts all .ogg files in a directory to .mp3
    """
    path = "data/"
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if ".ogg" in file:
                files.append(os.path.join(r, file))

    for file in files:
        ogg = AudioSegment.from_ogg(file)
        ogg.export(file.replace(".ogg", ".mp3"), format="mp3")
        os.remove(file)


convertFiles()
if __name__ == "__main__":
    app.run()
