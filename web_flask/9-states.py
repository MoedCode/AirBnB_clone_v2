#!/usr/bin/python3
"""starts a Flask web application:"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

APP = Flask(__name__)


@APP.route("/states", strict_slashes=False)
def list_states():
    """print a number"""
    states = storage.all(State)
    return render_template('9-states.html', states=states, states_only=True)


@APP.route("/states/<id>", strict_slashes=False)
def list_city_state(id):
    """display the state and it's cities"""
    result = []
    state_name = ''
    states = storage.all(State).values()
    cities = storage.all(City).values()
    for state in states:
        if state.id == id:
            state_name = state.name
    for city in cities:
        if id == city.state_id:
            result.append(city)
    return render_template('9-states.html',
                           result=result, states_only=False,
                           name=state_name)


@APP.teardown_appcontext
def cleanDb(error=None):
    """close the session"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
