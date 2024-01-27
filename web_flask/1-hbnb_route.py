#!/usr/bin/python3

"starts a Flask web application"
from flask import Flask

APP = Flask(__name__)

APP.url_map.strict_slashes = False


@APP.route("/")
def homepage():
    "Routing The Home Page"
    return "Hello HBNB!"


@APP.route("/hbnb")
def homepage():
    "Routing  HBNB Page"
    return "HBNB"


if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=5000)
