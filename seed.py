from model import db, connect_to_db, User, Team, UserTeam, Board
from sqlalchemy import func  # added to use func.max for fixing serial increment


def load_users():
    """Import and add user data from users.txt into db"""
    for row in open("seed-data/users.txt"):
        row = row.strip()
        user_data = row.split("|")
        if len(user_data) == 4:
            u_id, email, password, displayname = user_data
            user = User(u_id=u_id, email=email, password=password,
                        displayname=displayname)
        else:
            u_id, email, pw = user_data
            user = User(u_id=u_id, email=email, password=password)
        db.session.add(user)
        db.session.commit()


def load_teams():
    """Import and add team data from teams.txt into db"""
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
        user_id, team_id, joined = row.split("|")
        if joined == "t":
            joined = True
        else:
            joined = False
        userteam = UserTeam(user_id=user_id, team_id=team_id, joined=joined)
        db.session.add(userteam)
        db.session.commit()


def set_user_id_value_after_seed():
    """After test_data seeds, determines the user id start for
       serial increment (for dynamic user adds)."""

    max_u_id_tuple = db.session.query(func.max(User.u_id)).one()
        # returns a single value tuple >>> (int,)
    max_u_id = int(max_u_id_tuple[0])  # file may load with string, so this is a good idea

    query = "SELECT setval('user_accounts_u_id_seq', :start_id)"
        # uses setval() with arguments of the user_accounts table sequencer and a value for it (defined next)
            # setval() is a Sequence Manipulation Function, using a regclass and bigint input
            # https://www.postgresql.org/docs/8.1/static/functions-sequence.html
            # find the table sequencers with /ds in psql
    db.session.execute(query, {'start_id': (max_u_id + 1)})
        # runs query on db; dictionary required to pass the expression as the int for setval()
    db.session.commit()


if __name__ == "__main__":
    import os
    os.system('dropdb project')
    os.system('createdb project')
    
    from server import app
    connect_to_db(app)
    db.create_all()
    load_users()
    load_teams()
    load_userteams()
    set_user_id_value_after_seed()
