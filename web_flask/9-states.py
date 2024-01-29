#!/usr/bin/python3
"""0. Hello Flask!"""
from flask import Flask, render_template
from models.state import State
from models import storage


APP = Flask(__name__)
APP.url_map.strict_slashes = False

@APP.route("/states")
def listing_sates_id():
    states = storage.all(State).values()
    return render_template("7-states_list.html", states=states)


@APP.route("/states/<id>")
def state_id(id):
    state = None
    for each_St in storage.all(State).values():
        if each_St.id == id:
            state = each_St
            break
    return render_template("9-states.html", state=state)


@APP.teardown_appcontext
def close_db_sess(exception=None):
    storage.close()


if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=5000)
