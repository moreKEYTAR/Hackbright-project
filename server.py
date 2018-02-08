from flask import (Flask,  # Flask allows app object
                   session, flash,  # session allows use of session storage for login
                   render_template, redirect,  # render_template allows html render funcitonality
                   request,  # request allows use of forms in html templates
                   jsonify)
from flask_debugtoolbar import DebugToolbarExtension
import jinja2
from model import db, connect_to_db, User, Team, UserTeam, Board
    # Added to connect to data model classes
    # Previous version: from model import *

app = Flask(__name__)  # makes app object
app.secret_key = "It's great to stay up late"  # allows session use 'under the hood'
app.jinja_env.undefined = jinja2.StrictUndefined
    # Normally, if you refer to an undefined variable in a Jinja template,
    # Jinja silently ignores this. This makes debugging difficult, so we'll
    # set an attribute of the Jinja environment that says to make this an
    # error.

# import pdb; pdb.set_trace()


@app.route("/")
def index():
    """Return index (homepage)."""
    # How do I check for logged in status before rendering? People want to go back to the homepage
    return render_template("home.html")


@app.route("/users/new", methods=["POST"])
def make_new_user():
    """Validate new user form entry, register user if valid."""

    email = request.form.get('email')
    pw = request.form.get('pw')

    user_record = User.query.filter(User.email == email).first()
    # queries user table for first record with that email; returns None if no record
    if user_record is None:

        new_user = User(email=email, password=pw)
        db.session.add(new_user)
        db.session.commit()

        session["login"] = True
        session["new_user"] = True  # I want to use this for a tutorial or something later. How? How do we validate if the login is true on each page?
        user = User.query.filter(User.email == email).first()
        session["user_id"] = user.u_id
        flash("Account created. Awesome!")
        return redirect("/users/me/dashboard")

    else:
        flash("Oops...that email has already been used!")
        return redirect("/")


@app.route("/users/login", methods=["GET"])
def display_login():
    """Load login form."""

    return render_template("login.html")


@app.route("/users/login", methods=["POST"])
def log_in_returning_user():
    """Validate login entry."""

    # update login count to calculate attempts and remaining
    if session.get("login_count") is None:
        session["login_count"] = 1
    else:
        session["login_count"] += 1
    attempts = session["login_count"]
    max_attempts = 4
    remaining = max_attempts - attempts

    # grab login form data
    email = request.form.get('email')
    pw = request.form.get('pw')

    # pull user record for that email
    user_record = User.query.filter(User.email == email).first()

    if user_record is None:
        flash("No SamePage account found with that email. Time to register!")
    else:
        if user_record.password != pw:
            session["login"] = False
            if remaining <= 0:
                flash("Not really sure how pw security works. You could just clear your cache and I would never know. And what if you want to try a different address? This is complicated.")
                return render_template("password-recovery.html")
            elif remaining == 1:
                stringy_remaining = str(remaining)
                flash("You have " + stringy_remaining + " attempt remaining before account is locked.")
                flash("Not really sure how pw security works. You could just clear your cache and I would never know. And what if you want to try a different address? This is complicated.")
            else:
                stringy_remaining = str(remaining)
                flash("You have " + stringy_remaining + " attempts remaining before account is locked.")
                flash("Not really sure how pw security works. You could just clear your cache and I would never know. And what if you want to try a different address? This is complicated.")
            return redirect("/users/login")

        else:
            session["login"] = True
            user = User.query.filter(User.email == email).first()
            session["user_id"] = user.u_id
            session["login_count"] = 0
            flash("Welcome back to SamePage")
            return redirect("/users/me/dashboard")  # Successful login


@app.route("/users/login/password-recovery")
def password_recovery():
    """SOMETHING SOMETHING DARK SIDE"""

    return "OOOOOOOPS"


@app.route("/users/me/dashboard")
def dashboard():
    if session.get("new_user"):
        flash("New user! Tutorial time!")
    if session.get("login") is True:
        user_data_link_eager()
        user = get_user_object()
        # user_data = get_user_data(user)
        return render_template('dashboard.html')
    else:
        return redirect("/")


def get_user_object():
    """Queries db to return user object, using u_id saved in session"""
    user_id = session.get("user_id")
    user_object = User.query.get(user_id)
    return user_object


def user_data_link_eager():
    """Queries db to return user data by user object, front loading relationships"""
    users = User.query.options(db.joinedload("userteam")).all()
    return users
    # STILL WORKING


@app.route("/users/me/new-team")
def new_team():
    """Temporary page that forces name choice"""
    return render_template("make-new-team.html")


@app.route("/users/me/add-team", methods=["POST"])
def add_team():
    name = request.form.get("name")
    desc = request.form.get("description", None)
    user = get_user_object()

    new_team = Team(name=name, desc=desc)
    db.session.add(new_team)
    db.session.commit()

    new_userteam = UserTeam(user_id=user.u_id, team_id=new_team.t_id)
    db.session.add(new_userteam)
    db.session.commit()
    flash("yaaaaaay")
    return redirect("/users/me/dashboard")


@app.route("/users/me/logout", methods=["POST"])
def logout_user():
    session.clear()

    flash("You have been logged out.")
    return redirect("/")


if __name__ == "__main__":

    # make sure templates, etc. are not cached in debug mode
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # prevents server side caching

    connect_to_db(app)  # model file houses all ORM, so importing that funciton to connect to db

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host='0.0.0.0')  # DO NOT FORGET TO CHANGE THIS IF RELEASING WEB APP
    # Is this the same as app.debug = True?????
    # Does order matter???
