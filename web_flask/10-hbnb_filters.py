#!/usr/bin/python3
"""0. Hello Flask!"""
from flask import Flask, render_template
from models.state import State
from models.amenity import Amenity
from models import storage



APP = Flask(__name__)
APP.url_map.strict_slashes = False

@APP.route("/hbnb_filters")
def lists_states_cls():
    data = {
    'states' : storage.all(State).values(),
    'amenities': storage.all(Amenity).values()
    }
    return render_template("10-hbnb_filters.html", models=data)


@APP.teardown_appcontext
def close_db(exception=None):
    storage.close()


if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=5000)
