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
app.jinja_env.auto_reload = True
    # Suggested in Slack #boooooo channel, to fix an error that will sometimes happen
        # where some versions of Flask bug so that you have to re-start your server
        # with every change on your template.

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
        return redirect("/users/{}/dashboard".format(user.u_id))

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
            return redirect("/users/{}/dashboard".format(user.u_id))
                # Successful login redirects to dashboard with customized url


@app.route("/users/login/password-recovery")
def password_recovery():
    """SOMETHING SOMETHING DARK SIDE"""

    return "OOOOOOOPS"


@app.route("/users/<int:user_id>/dashboard")
def dashboard(user_id):
    """Renders dashboard view, grabbing existing teams for display"""
    if session.get("new_user"):
        flash("New user! Tutorial time!")
    if session.get("login") is True:
        teams_list = []
        user_id = session.get("user_id")
        user_object = User.query.get(user_id)
        ut_objects = user_object.userteams  # makes a list of objects
        for userteam in ut_objects:
            team_dict = {"team_id": userteam.team_id,
                         "name": userteam.team.name,
                         "desc": userteam.team.desc,
                         "is_member": userteam.is_member}
            teams_list.append(team_dict)
        return render_template('dashboard.html', teams_list=teams_list)
    else:
        return redirect("/")  # Prevents view if not logged in


@app.route("/users/<int:user_id>/<int:team_id>")
def view_team(user_id, team_id):
    """Renders view of team page, with board"""
    if session.get("user_id") == user_id:  # validates for current logged in user
        boards_dict = {}
        boards = Board.query.filter_by(team_id=team_id).all()  # BaseQuery object

        return "UAAAAAAA YIPPPEEEEE"

    # if session.get("login") is True:
    #     teams_list = []
    #     user_id = session.get("user_id")
    #     user_object = User.query.get(user_id)
    #     ut_objects = user_object.userteams  # makes a list of objects
    #     for userteam in ut_objects:
    #         team_dict = {"team_id": userteam.team_id,
    #                      "name": userteam.team.name,
    #                      "desc": userteam.team.desc,
    #                      "is_member": userteam.is_member}
    #         teams_list.append(team_dict)
    #     return render_template('dashboard.html', teams_list=teams_list)
    else:
        return "ooooh noooooo"  # Prevents view if not logged in



@app.route("/users/<int:user_id>/new-team")
def new_team(user_id):
    """Temporary page that forces name choice"""
    return render_template("make-new-team.html")


@app.route("/users/<int:user_id>/add-team", methods=["POST"])
def add_team(user_id):
    """"""
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
    return redirect("/users/{}/dashboard".format(user.u_id))


@app.route("/users/<int:user_id>/logout", methods=["POST"])
def logout_user(user_id):
    session.clear()

    flash("You have been logged out.")
    return redirect("/")

###############################FROM RATINGS ###############################
# @app.route("/movies/<int:movie_id>", methods=['POST'])
# def movie_detail_process(movie_id):
#     """Add/edit a rating."""

#     # Get form variables
#     score = int(request.form["score"])

#     user_id = session.get("user_id")
#     if not user_id:
#         raise Exception("No user logged in.")  #### WHAT IS THIS ####

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
