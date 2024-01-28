#!/usr/bin/python3
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)

@app.route("/cities_by_states", strict_slashes=False)
def states_listing():
    """List states"""
    states_list = storage.all(State)
    return render_template("7-states_list.html", states=states_list)

@app.teardown_appcontext
def close_session(error=None):
    """Close the session"""
    storage.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
