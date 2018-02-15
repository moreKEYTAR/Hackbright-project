from flask import (Flask,  # Flask allows app object
                   session, flash,  # session allows use of session storage for login
                   render_template, redirect,  # render_template allows html render functionality
                   request,  # request allows use of forms in html templates
                   jsonify)
from flask_debugtoolbar import DebugToolbarExtension
import jinja2
from model import db, connect_to_db, User, Team, UserTeam, Board
from query import *
from helper import *

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


###########################################################################
# INDEX ###################################################################

@app.route("/")
def index():
    """Return index (homepage)."""
    # How do I check for logged in status before rendering?
    # What do I want to show for people who are logged in?
    return render_template("home.html")


###########################################################################
# REGISTRATION ############################################################

@app.route("/users/new", methods=["POST"])
def make_new_user():
    """Validate new user form entry, register user if valid."""

    email = request.form.get('email')
    pw = request.form.get('pw')

    user_record = User.query.filter(User.email == email).first()
    # queries user table for first record for email; returns None if no record
    if user_record is None:

        new_user = make_user(email, pw)
        add_to_db(new_user)

        user = get_user_by_email(email)
        update_session_for_good_login(user.u_id)

        session["new_user"] = True  # Pending: Tutorial
        flash("Account created. Awesome!")
        return redirect("/users/{}/dashboard".format(user.u_id))

    else:
        flash("Oops...that email has already been registered!")
        return redirect("/")

###########################################################################
# LOG IN ##################################################################

@app.route("/users/login", methods=["GET"])
def display_login():
    """Load login form."""

    return render_template("login.html")


@app.route("/users/login", methods=["POST"])
def log_in_returning_user():
    """Validate login entry."""

    # update login count to calculate attempts and remaining
    num_attempts = get_login_attempts()  # in helper.py
    remaining = calc_attempts_remaining(num_attempts)

    # getting data from user input in login.html form
    email = request.form.get('email')
    pw = request.form.get('pw')

    user_record = get_user_by_email(email)  # in query.py

    if user_record is None:
        flash("No account found with that email. Would you like to register?")
        return redirect("/users/login")

    else:  # the email is valid

        # validate password, handle accordingly
        if user_record.password != pw:
            template = handle_bad_attempts(remaining)  # in helper.py
            return render_template(template)

        # is valid password, handle accordingly
        else:
            update_session_for_good_login(user_record.u_id)
            flash("Welcome back to SamePage")
            return redirect("/users/{}/dashboard".format(user_record.u_id))


 # LOGIN: PASSWORD HANDLING ##############################################

@app.route("/users/login/password-recovery")
def password_recovery():
    """SOMETHING SOMETHING DARK SIDE"""

    return "OOOOOOOPS"


###########################################################################
# DASHBOARD ###############################################################

@app.route("/users/<int:user_id>/dashboard")
def dashboard(user_id):
    """Renders dashboard view, grabbing existing teams for display"""

    if session.get("new_user"):
        flash("New user! Tutorial time!")

    if session.get("login") is True:
        teams_list = []
        user_id = session.get("user_id")
        user_object = get_user_object(user_id)

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


@app.route("/users/<int:user_id>/new-team")
def new_team(user_id):
    """Temporary page that forces name choice"""

    return render_template("temp-new-team.html")


@app.route("/users/<int:user_id>/add-team", methods=["POST"])
def add_team(user_id):
    """Create Team model and UserTeam model, updating database each time."""

    name = request.form.get("name")
    desc = request.form.get("description", None)

    user = get_user_object(user_id)  # in query.py

    #  Should the following 4 lines be one function??
    new_team = make_team(name, desc)
    # team should not be made without also making a userteam (see below);
        # userteam requires team id
    add_to_db(new_team)

    new_userteam = make_userteam(user.u_id, new_team.t_id)
    add_to_db(new_userteam)

    flash("yaaaaaay")
    return redirect("/users/{}/dashboard".format(user.u_id))


@app.route("/users/<int:user_id>/join-team-<int:team_id>", methods=["POST"])
def join_team(user_id, team_id):
    """Update UserTeam to accept membership; redirect to temporary page to
    simulate pop up redirect."""

    is_valid = is_valid_url(user_id, team_id)

    if is_valid:
        update_userteam_accepted(user_id, team_id)
        return render_template("temp-join-team.html",
                               user_id=user_id, team_id=team_id)
    else:
        flash("Invalid user and team combo; no invites found!")
        return redirect("/users/{}/dashboard".format(user_id))


@app.route("/users/<int:user_id>/ignore-invite-<int:team_id>",
           methods=["POST"])
def ignore_team(user_id, team_id):
    """Update UserTeam to ???????????????????????????????????????????"""

    return ("WELL yOU Can'T IGnORe it")


###########################################################################
# TEAM VIEW ###############################################################

@app.route("/users/<int:user_id>/<int:team_id>")
def view_team(user_id, team_id):
    """Renders view of team page, with board"""

    if session.get("user_id") == user_id:
        team_object = Team.query.filter_by(t_id=team_id).first()
        boards_list = []
        if team_object:
            # checking for the team being a valid team
                # (in case it is manually forced into url)
            team_dict = {"t_id": team_id,
                         "name": team_object.name,
                         "desc": team_object.desc}  # new dictionary
            boards = Board.query.filter_by(team_id=team_id).all()  # list of objects
            if boards:  # checks for whether any board object in the list
                for board in boards:
                    boards_list.append({"b_id": board.b_id,
                                        "name": board.name,
                                        "desc": board.desc,
                                        "updated": board.updated})
            return render_template('team-main.html',
                                   boards=boards_list,
                                   team=team_dict)
        else:
            return "No team found with that information."

    else:  # Prevents view if not logged in
        flash("You do not have permission to view that page.")
        user_id = session["user_id"]
        return redirect("/users/{}/dashboard".format(user_id))


###########################################################################
# LOG OUT #################################################################

@app.route("/users/<int:user_id>/logout", methods=["POST"])
def logout_user(user_id):
    session.clear()

    flash("You have been logged out.")
    return redirect("/")


@app.route("/users/temp/logout", methods=["POST"])
def temp_logout():
    session.clear()
    flash("You have been logged out from temp logout route.")
    return redirect("/")


###########################################################################
# DIRECT FILE CALL ########################################################

if __name__ == "__main__":

    app.debug = True
    # prevents server side caching while in debug mode?
    app.jinja_env.auto_reload = app.debug  

    connect_to_db(app)  # model file houses all ORM
    DebugToolbarExtension(app)  # Use the DebugToolbar
    app.run(host='0.0.0.0')  # DO NOT FORGET TO CHANGE THIS FOR RELEASE
