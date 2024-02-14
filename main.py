from flask import Flask, render_template
import practice_utils

from werkzeug.middleware.proxy_fix import ProxyFix

import os
app = Flask(__name__)
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

@app.get("/")
def index():
    image_dir = "media/index"
    images = os.listdir(os.path.join(app.static_folder, image_dir))
    return render_template('index_v5.html', images=images, image_dir=image_dir)

@app.get("/kontakt")
def contacts():
    image_dir = "media/contacts"
    images = os.listdir(os.path.join(app.static_folder, image_dir))
    return render_template('kontakt.html', images=images, image_dir=image_dir)

@app.get("/treninky")
def practices():
    image_dir = "media/practices"
    images = os.listdir(os.path.join(app.static_folder, image_dir))
    practices = practice_utils.get_trainings()
    return render_template('treninky.html', practices=practices, images=images, image_dir=image_dir)

@app.get("/tym")
def team():
    image_dir = "media/about"
    images = os.listdir(os.path.join(app.static_folder, image_dir))
    return render_template("team.html", images=images, image_dir=image_dir)

@app.get("/ultimate")
def ultimate():
    image_dir = "media/ultimate"
    images = os.listdir(os.path.join(app.static_folder, image_dir))
    return render_template('ultimate.html', images=images, image_dir=image_dir)

if __name__ == '__main__':
    app.run()
