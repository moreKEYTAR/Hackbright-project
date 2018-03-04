from model import (db, connect_to_db,
                   User, Team, UserTeam, Board, Project, Phase)
from sqlalchemy import func  # added to use func.max for fixing serial increment
# import pdb; pdb.set_trace()


def load_users():
    """Import and add user data from users.txt into db"""
    # All data in users.txt should have a u_id already, and may or may not
        # have a displayname

    for row in open("seed-data/users.txt"):
        row = row.strip()
        user_data = row.split("|")
        if len(user_data) == 4:
            u_id, email, password, displayname = user_data
            user = User(u_id=u_id, email=email, password=password,
                        displayname=displayname)
        else:  # Assuming the only other case for test data to be
                    # missing a displayname
            u_id, email, password = user_data
            user = User(u_id=u_id, email=email, password=password)

        db.session.add(user)
        db.session.commit()

    set_user_id_value_after_seed()


def load_teams():
    """Import and add team data from teams.txt into db"""
    # All data in teams.txt SHOULD have a description, but that data is
        # optional for user creating a table.

    for row in open("seed-data/teams.txt"):
        row = row.strip()
        name, desc = row.split("|")
        team = Team(name=name, desc=desc)

        db.session.add(team)
        db.session.commit()


def load_userteams():
    """Import and add userteam data from userteams.txt into db"""

    for row in open("seed-data/userteams.txt"):
        row = row.strip()
        userteam_data = row.split("|")
        if len(userteam_data) == 3:
            user_id, team_id, is_member = userteam_data
            if is_member == "t":
                is_member = True
            else:
                is_member = False  # the invite was rejected
            userteam = UserTeam(user_id=user_id, team_id=team_id,
                                is_member=is_member)
        elif len(userteam_data) == 2:
            user_id, team_id = userteam_data
            userteam = UserTeam(user_id=user_id, team_id=team_id)

        db.session.add(userteam)
        db.session.commit()


def load_boards():
    """Import and add boards data from boards.txt into db"""

    for row in open("seed-data/boards.txt"):
        row = row.strip()
        board_data = row.split("|")
        if len(board_data) == 3:
            team_id, name, desc = board_data
            new_board = Board(team_id=team_id, name=name, desc=desc)
        elif len(board_data) == 2:
            team_id, name = board_data
            new_board = Board(team_id=team_id, name=name)

        db.session.add(new_board)
        db.session.commit()


def load_phases():
    """Import and add project phases from phases.txt into db"""
    for row in open("seed-data/phases.txt"):
        ph_code = row.strip()
        new_phase = Phase(ph_code=ph_code)
        db.session.add(new_phase)
        db.session.commit()


def load_projects():
    """Import and add projects data from projects.txt into db"""

    for row in open("seed-data/projects.txt"):
        row = row.strip()
        # '4||idea|Reassemble Riverlands armies under Sansa||2|'
        project_data = row.split("|")
        # ['4', '', 'idea', 'Reassemble Riverlands armies under Sansa',
            #  '', '2', '']

        board_id = project_data[0]

        user_id = project_data[1]

        if not user_id:
            user_id = None  # is this explicitly needed?

        phase_code = project_data[2]

        title = project_data[3]

        notes = project_data[4]
        if not notes:
            notes = None

        upvotes = project_data[5]
        if not upvotes:
            upvotes = None

        updated = project_data[6]
        if not updated:
            updated = datetime.utcnow()
        new_project = Project(board_id=board_id, user_id=user_id,
                              phase_code=phase_code, title=title,
                              notes=notes, upvotes=upvotes,
                              updated=updated)

        db.session.add(new_project)
        db.session.commit()


def set_user_id_value_after_seed():
    """After test_data seeds, determines the user id start for
       serial increment (for dynamic user adds)."""

    max_u_id_tuple = db.session.query(func.max(User.u_id)).one()
        # returns a single value tuple >>> (int,)
    max_u_id = int(max_u_id_tuple[0])
        # file may load with string, so this is a good idea
    query = "SELECT setval('user_accounts_u_id_seq', :start_id)"
        # uses setval() with arguments of the user_accounts table sequencer
        # and a value for it (defined next)
            # setval() is a Sequence Manipulation Function,
                # using a regclass and bigint input
            # https://www.postgresql.org/docs/8.1/static/functions-sequence.html
                # find the table sequencers with /ds in psql
    db.session.execute(query, {'start_id': max_u_id})
        # runs query on db; dictionary required to pass the expression
            # as the int for setval()
    db.session.commit()


if __name__ == "__main__":
    # import os
    # os.system('dropdb project')
    # os.system('createdb project')

    from server import app
    connect_to_db(app)
    print "Connected to DB."
    # db.drop_all()
    db.create_all()  # Create class models, which have been imported from model.py
    load_users()  # Runs set_user_id_value_after_seed() as well
    load_teams()
    load_userteams()
    load_boards()
    load_phases()
    load_projects()

    print "DB re-seed successful."

