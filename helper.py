from flask import (Flask,  # Flask allows app object
                   session, flash,  # session allows use of session storage for login
                   render_template, redirect,  # render_template allows html render functionality
                   request,  # request allows use of forms in html templates
                   jsonify)
from flask_debugtoolbar import DebugToolbarExtension

# don't need to import app, right?


# LOGIN HELPERS ##########################################################

def is_logged_in():
    """Check session for login status"""
    if session.get("login") is True:
        return True
    else:
        return False


def get_user_id_from_session():
    """Queries session dictionary for user id (integer)
        - should be called only if is_logged_in() returns True
    """
    user_id = session.get("login")
    return user_id


def get_login_attempts():
    """Creates or updates login count tracker in the session."""

    if session.get("login_count") is None:  # Checks whether key exists
        session["login_count"] = 1
    else:
        session["login_count"] += 1

    return session["login_count"]


def calc_attempts_remaining(login_count):
    """Taking in an integer count, Returns number of remaining attempts."""

    max_attempts = 4
    remaining = max_attempts - login_count
    return remaining


def update_session_for_good_login(user_id):
    """Takes in integer for user id, updates session, returns nothing."""
    session["user_id"] = user_id
    session["login"] = True
    session["login_count"] = 0
    print "Session updated; logged in."


def handle_bad_attempts(remaining):
    """Gives proper path after user attempts and fails to log in:
        - Takes in login attempts remaining
        - Sets the session key login
        - Gives user flash feedback
        - Returns a string for the template to render"""

    session["login"] = False

    if remaining <= 0:   # handling for negative numbers... still
                         # testing to see if this is possible to create.
        flash("""PASSWORD SECURITY FEATURE PENDING.
             Login attempts not linked to IP address or a specific email.
              Does cache matter? This is complicated.""")
        path = "password-recovery.html"

    elif remaining == 1:
        stringy_remaining = str(remaining)
        flash("You have " + stringy_remaining +
              " attempt remaining before account is locked.")
        flash("""PASSWORD SECURITY FEATURE PENDING.
             Login attempts not linked to IP address or a specific email.
              Does cach matter? This is complicated.""")
        path = "login.html"

    else:  # separate path to make sure user flash feedback is plural
        stringy_remaining = str(remaining)
        flash("You have " + stringy_remaining +
              " attempts remaining before account is locked.")
        flash("""PASSWORD SECURITY FEATURE PENDING.
             Login attempts not linked to IP address or a specific email.
              Does cach matter? This is complicated.""")
        path = "login.html"

    return path


# AUTHORIZED FOR VIEW BY URL #############################################

def is_valid_user_in_url(url_user_id):
    """Checks user id in url against the user id in the session"""

    logged_in = is_logged_in()  # checks logged in

    if logged_in:
        u_id = get_user_id_from_session()

        if u_id == url_user_id:
            return True

    return False
