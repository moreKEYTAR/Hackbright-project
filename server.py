###########################################################################
# IMPORTS - GEN ###########################################################

from flask import (Flask,
                   # Flask allows app object
                   session, flash,
                   # session allows use of session storage for login
                   render_template, redirect,
                   # render_template allows html render functionality
                   request,
                   # request allows use of forms in html templates
                   jsonify)
from flask_debugtoolbar import DebugToolbarExtension
import jinja2
from model import (db, connect_to_db,
                   User, Team, UserTeam, Board, Project, Phase)
import query as q
import helper as h

# import pdb; pdb.set_trace()


###########################################################################
# FLASK APP SETUP #########################################################

app = Flask(__name__)  # makes app object
app.secret_key = "It's great to stay up late"
    # allows session use 'under the hood'

app.jinja_env.undefined = jinja2.StrictUndefined
    # Normally, if you refer to an undefined variable in a Jinja template,
        # Jinja silently ignores this. "This makes debugging difficult, so
        # we'll set an attribute of the Jinja environment that says to make
        # this an error.""
app.jinja_env.auto_reload = True
    # Fixes error that will sometimes happen where (in some versions of Flask)
        # you have to re-start your server with every change on your template.


###########################################################################
# SESSION STORAGE #########################################################

# Keys:
    # "login" (bool)
    # "user_id" (int)
    # "team_id" (int)
    # "new_user" (bool)


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

@app.route("/register", methods=["POST"])
def make_new_user():
    """Validate new user form entry, register user if valid."""

    email = request.form.get('email')
    pw = request.form.get('pw')

    user_record = User.query.filter(User.email == email).first()
    # queries user table for first record for email; returns None if no record
    if user_record is None:

        new_user = q.make_user(email, pw)
        q.add_to_db(new_user)

        user = q.get_user_by_email(email)
        h.update_session_for_good_login(user.u_id)

        session["new_user"] = True  # Pending: Tutorial
        flash("Account created. Awesome!")
        return redirect("/users/{}/dashboard".format(user.u_id))

    else:
        flash("Oops...that email has already been registered!")
        return redirect("/")


###########################################################################
# LOG IN ##################################################################

@app.route("/login", methods=["GET"])
def display_login():
    """Load login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def log_in_returning_user():
    """Validate login entry."""

    # update login count to calculate attempts and remaining
    num_attempts = h.get_login_attempts()
    remaining = h.calc_attempts_remaining(num_attempts)

    # getting data from user input in login.html form
    email = request.form.get('email')
    pw = request.form.get('pw')

    user_record = q.get_user_by_email(email)

    if user_record is None:
        flash("No account found with that email. Would you like to register?")
        return redirect("/login")

    else:  # the email is valid

        # validate password, handle accordingly
        if user_record.password != pw:
            template = h.handle_bad_attempts(remaining)
            return render_template(template)

        # is valid password, handle accordingly
        else:
            h.update_session_for_good_login(user_record.u_id)
            flash("Welcome back to SamePage")
            return redirect("/dashboard")


 # LOGIN: PASSWORD HANDLING ##############################################

@app.route("/login/password-recovery")
def password_recovery():
    """Displays form to send email to user for password recovery"""

    return "OOOOOOOPS"


###########################################################################
# DASHBOARD ###############################################################

@app.route("/dashboard")
def dashboard():
    """Renders dashboard view, grabbing existing teams for display"""

    session["team_id"] = None
        # Creates a session key for team_id, which is needed in the new board
        # route, and therefore must be reset.

    if session.get("new_user"):
        flash("New user! Tutorial time! NEED TO MAKE POP UP")

    if session.get("login") is True:
        # Fossil from validation version; does not hurt to keep
        teams_list = []
        invites_list = []
        user_id = session.get("user_id")
        user_object = q.get_user_object(user_id)

        ut_objects = user_object.userteams  # makes a list of objects
        for userteam in ut_objects:
            if userteam.is_member:
                team_dict = {"team_id": userteam.team_id,
                             "name": userteam.team.name,
                             "desc": userteam.team.desc}
                teams_list.append(team_dict)
            elif userteam.is_member is None:
            # null value means invite decision pending
                invite_dict = {"team_id": userteam.team_id,
                               "name": userteam.team.name,
                               "desc": userteam.team.desc}
                invites_list.append(invite_dict)

        return render_template('dashboard.html', teams_list=teams_list,
                               invites_list=invites_list)

    else:
        return redirect("/")
            # Prevents view if not logged in
            # Fossil from validation version; does not hurt to keep


@app.route("/new-team", methods=["POST"])
def create_team():
    """Create Team model and UserTeam model, updating database each time."""

    name = request.form.get("name", "Untitled")
    desc = request.form.get("description", None)

    user_id = session.get("user_id")

    new_team = q.make_team(name, desc)
    q.add_to_db(new_team)

    # We now have the team id, so we can make the UserTeam relationship
    new_userteam = q.make_userteam(user_id, new_team.t_id)
    q.add_to_db(new_userteam)

    # flash("Team created! MAKE POPUP TO ASK To GO STRAIGHT TO THE TEAM PAGE")
    return jsonify({"teamId": new_team.t_id})


@app.route("/team-invitation", methods=["POST"])
def update_team_membership():
    """Update UserTeam membership field's value to true;
    update Dashboard with a redirect."""

    # This route is currently in contrast to the style of making a new team,
        # which is an ajax request.
    user_id = session["user_id"]
    team_id = request.form.get("team")
    user_choice = request.form.get("is_joining")
        # in dashboard.html hidden value; True or False

    # Cleanse data from html as soon as possible
    if user_choice == "True":
        user_choice = True  # this line doesn't work
    else:
        user_choice = False

    q.update_userteam_relationship(user_id, team_id, user_choice)

    flash("Your team invites have been updated!")

    return redirect("/dashboard")


@app.route("/ignored-teams", methods=["GET"])
def display_ignored_teams():
    """PENDING PENDING PENDING"""
    return "Pending my good lady"


###########################################################################
# TEAM MAIN AND BOARDS ####################################################

@app.route("/view-team")
def view_team():
    """Renders view of team page, with board"""

    team_id = session.get("team_id")

    if team_id is None:
        team_id = request.args.get("team")
        session["team_id"] = team_id

    team_object = Team.query.filter_by(t_id=team_id).first()  # REFACTOR THIS

    return render_template("team-main.html", team=team_object)


@app.route("/new-board", methods=["POST"])
def make_new_board():
    """Make a new board and update page without refresh; ajax."""

    ##### VALIDATION HERE PLEASE ######
    user_id = session.get("user_id")

    name = request.form.get("new-board-name", "Untitled")  # board's name input
        # Is this a good way to handle not requiring the team or board name
            # in the form, but in the data fields?
    desc = request.form.get("new-board-desc", None)  # board's desc input
    team_id = request.form.get("team-id")

    session["team_id"] = team_id
    # Not sure if I need this; it should already be there, but this keeps it
        # current

    new_board = q.make_board(name, desc, team_id)
    q.add_to_db(new_board)

    flash("Board created! MAKE THAT BOARD SHOW AS DEFAULT!!!!")
    return redirect("/view-team")


@app.route("/claim-project", methods=["POST"])
def assign_user_to_project():
    """Update database with user_id for the project."""

    user_id = session.get("user_id")
    project_id = request.form.get("projectId")

    q.update_user_claiming_project(user_id, project_id)

    return "HTTP-status-code: 200"


###########################################################################
# LOG OUT #################################################################

@app.route("/logout", methods=["POST"])
def logout_user():

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
