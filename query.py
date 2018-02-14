
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from model import db, connect_to_db, User, Team, UserTeam, Board


# OBJECT QUERIES #########################################################

def get_user_object(u_id):
    """Takes in an integer and queries the user_accounts table for that
    user object."""

    user = User.query.get(u_id)
    return user


def update_db(baseobject):
    """Takes in any Model object and adds it to the database,
    committing the update."""

    db.session.add(baseobject)
    db.session.commit()
    print "Added to db."
