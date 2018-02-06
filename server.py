from flask import Flask, render_template, session, flash, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
import jinja2
# Flask allows app object
# render_template allows html render funcitonality
# session allows use of session storage for login
# request allows use of forms in html templates

import model  # Added to connect to data model classes
              # Alternative: from model import connect_to_db, db

app = Flask(__name__)  # makes app object
app.secret_key = "It's great to stay up late"  # allows session use 'under the hood'

app.jinja_env.undefined = jinja2.StrictUndefined
# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.
model.connect_to_db(app)  # Why isn't this in the dunder name equals main?
# model file houses all ORM, so importing that funciton to connect to db

@app.route("/")
def index():
    """Return index (homepage)."""

    return render_template("home.html")

# @app.route("")

if __name__ == "__main__":

    # make sure templates, etc. are not cached in debug mode
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host='0.0.0.0')  # DO NOT FORGET TO CHANGE THIS IF RELEASING WEB APP
    # Is this the same as app.debug = True?????
    # Does order matter???
