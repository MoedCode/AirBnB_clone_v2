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
def HBNBpage():
    "Routing  HBNB Page"
    return "HBNB"


@APP.route("/c/<str>")
def display_c(str):
    "display string argument in url"
    str_tok = str.replace('_', ' ')
    return f"C {str_tok}"


@APP.route("/python")
@APP.route("/python/<str>")
def display_py(str="is cool"):
    "display string argument in url"
    str_tok = str.replace('_', ' ')
    return f"Python {str_tok}"


if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=5000)
