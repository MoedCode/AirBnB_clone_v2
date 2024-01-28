#!/usr/bin/python3
"""starts a Flask web APPlication:"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

APP = Flask(__name__)


@APP.route("/cities_by_states", strict_slashes=False)
def list_states():
    """List states"""
    states_list = storage.all(State)
    cities_list = storage.all(City)
    return render_template('8-cities_by_states.html',
                           states=states_list, cities=cities_list)


@APP.teardown_APPcontext
def cleanDb(error=None):
    """close the session"""
    storage.close()


if __name__ == "__main__":
    APP.run(host='0.0.0.0', port=5000)
