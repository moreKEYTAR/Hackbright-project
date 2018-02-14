from flask import (Flask,  # Flask allows app object
                   session, flash,  # session allows use of session storage for login
                   render_template, redirect,  # render_template allows html render functionality
                   request,  # request allows use of forms in html templates
                   jsonify)
from flask_debugtoolbar import DebugToolbarExtension

# don't need to import app, right?


# LOGIN CHECKERS #########################################################

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


def is_valid_user_in_url(url_user_id):
    """Checks user id in url against the user id in the session"""

    logged_in = is_logged_in()  # checks logged in

    if logged_in:
        u_id = get_user_id_from_session()

        if u_id == url_user_id:
            return True

    return False