"""Queries to database and updates to database, as abstracted from server.py """

from model import (db, connect_to_db,
                   User, Team, UserTeam, Board, Project, Phase)


# MAKE NEW OBJECT #######################################################

def make_user(email, password, displayname, is_registered=True):
    """Takes in registration form strings, makes a User object, returns it."""

    new_user = User(email=email, password=password, displayname=displayname,
                    is_registered=is_registered)
    return new_user


def make_team(t_name, t_desc):
    """Takes in string parameters, makes a Team object, returns it."""

    new_team = Team(name=t_name, desc=t_desc)
    return new_team


def make_userteam(u_id, t_id):
    """Takes in integer parameters, makes a UserTeam object, returns it."""

    new_userteam = UserTeam(user_id=u_id, team_id=t_id, is_member=True)
    return new_userteam


def make_board(b_name, b_desc, t_id):
    """Takes in two strings and an integer, makes a Board object, returns it."""

    new_board = Board(team_id=t_id, name=b_name, desc=b_desc)
    return new_board


def make_project(p_title, p_notes, p_phase, b_id):
    """Takes in three strings and an integer,
    makes a Project object, returns it."""

    new_project = Project(board_id=b_id, phase_code=p_phase, title=p_title,
                          notes=p_notes)
    return new_project


# UPDATE DATABASE #######################################################

def add_to_db(baseobject):
    """Takes in any Model object and adds it to the database,
    committing the update."""

    db.session.add(baseobject)
    db.session.commit()
    print "Added to db; db update committed."


def update_userteam_relationship(u_id, t_id, u_choice):
    """Uses ids and boolean to update UserTeam object"""

    userteam = get_userteam_object(u_id, t_id)
    userteam.is_member = u_choice
    db.session.commit()
    print "Membership on team is updated in db."


def update_user_claiming_project(u_id, p_id):
    """Uses ids to update ownership of a project, and assigns the 'item' phase,
        as ideas can currently be claimed too."""

    project = get_project_object(p_id)
    project.user_id = u_id
    project.phase_code = "item"
    db.session.commit()
    print """The project ownership is updated to the user {} and
    project {}""".format(u_id, p_id)


# OBJECT QUERIES #########################################################

def get_user_object(u_id):
    """Takes in an integer and queries the user_accounts table for that
    user object."""

    user = User.query.get(u_id)
    return user


def get_userteam_object(u_id, t_id):
    """Takes in an integer and queries the user_accounts table for that
    user object."""

    userteam = UserTeam.query.filter(UserTeam.user_id == u_id,
                                     UserTeam.team_id == t_id).first()
    return userteam


def get_project_object(p_id):
    """Takes in an integer and queries the projects table."""

    project = Project.query.get(p_id)

    return project


# FETCH INSTANCE QUERIES (WITH FIRST) ####################################

def get_user_by_email(email):
    """Filters for user record by email, returning None if not present."""

    user = User.query.filter(User.email == email).first()

    return user


# GET ALL OBJECTS QUERRIES ###############################################

def get_projects_by_user(u_id):
    """Retrieves all project objects for the given user."""

    projects = Project.query.filter(Project.user_id == u_id).all()

    return projects


def get_projects_for_chart_A(t_id, start_dt, end_dt):
    """Retrieves completed project datetimes for Chart A by team and within
    datetime range."""

    all_chartable_projects = []

    board_objects = db.session.query(Board.b_id).filter(Board.team_id == t_id)

    for board in board_objects:
        # b_id = board_tup[0]
        # projects = Board.query.get(b_id).projects
        projects = db.session.query(Project.updated).filter(
                    Project.board_id == board.b_id)
        chartable_projects = projects.filter(
                                (Project.updated >= start_dt) &
                                (Project.updated < end_dt) &
                                (Project.phase_code == "done"))
        all_chartable_projects.extend(chartable_projects.all())

    # all_chartable_projects is a list of objects (all are unique)
    return all_chartable_projects

# {"data": [200, 168, 456, 321, 109, 88, 149],

# import pdb; pdb.set_trace()



######################################################################
######################################################################

if __name__ == "__main__":

    from server import app
    # As a convenience, if we run this module interactively, it will leave
        # you in a state of being able to work with the database directly.
    connect_to_db(app)
    print "Connected to DB."
