"""Models and database functions for database called project."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func  # added to use func.max for fixing serial increment
from datetime import datetime
# import query  # Added this to access query functions. Needed???

db = SQLAlchemy()  # Creates db object; already ran createdb project in bash

###################################################################


class User(db.Model):
    """User model"""

    __tablename__ = "user_accounts"

    u_id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                     nullable=False, unique=True)
    email = db.Column(db.String(254), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False, unique=True)
    # password_salt = db.Column(db.String(50), nullable=False)
    # password_hash_algorithm = db.Column(db.String(50), nullable=False)


    # Can you have nullable=False, if you want to add it after registration????


    displayname = db.Column(db.String(30), nullable=True, unique=False)
    # fname = db.Column(db.String(30), nullable=True, unique=False)  # MAY NEED TO RECONSIDER
    # lname = db.Column(db.String(50), nullable=True, unique=False)  # MAY NEED TO RECONSIDER
    userteam = db.relationship("UserTeam")

    ###### User - projects relationship needs work ###################
    # authored_project = db.relationship("Project")  # Backref is "author"
    # claimed_project = db.relationship("Project")  # Backref is "claimer"

    def __repr__(self):
        """Provide useful output when printing: User."""

        return "<{email}  U_ID: {u_id}  Displayname: {display}>".format(
            email=self.email, u_id=self.u_id, display=self.displayname)


class Team(db.Model):
    """Team model"""

    __tablename__ = "team_accounts"

    t_id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                     nullable=False, unique=True)
    # email = db.Column(db.String(254), nullable=False, unique=True)
    # password = db.Column(db.String(200), nullable=False, unique=True)
    # password_salt = db.Column(db.String(50), nullable=False)
    # password_hash_algorithm = db.Column(db.String(50), nullable=False)
    # displayname = db.Column(db.String(20), nullable=False, unique=False)
    name = db.Column(db.String(100), nullable=False, unique=False)  # MAY NEED TO RECONSIDER
    desc = db.Column(db.String(255), nullable=True, unique=False)  # MAY NEED TO RECONSIDER
    userteam = db.relationship("UserTeam")  # backref is "team"

    ############ Board - team relationship needs work ##############
    board = db.relationship("Board")  # Backref is "team"
        # Many boards to one team; returns MANY things

    def __repr__(self):
        """Provide useful output when printing: Team."""

        return "<{name}  T_ID: {t_id}>".format(name=self.name, t_id=self.t_id)


class UserTeam(db.Model):
    """UserTeam model, with joined status"""

    __tablename__ = "users_teams"

    ut_id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                      nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_accounts.u_id'),
                        nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team_accounts.t_id'),
                        nullable=False)
    joined = db.Column(db.Boolean, nullable=False, default=False)
        # joined is whether the user has accepted to be one a team

    user = db.relationship("User")  # Backref is "userteam"
    team = db.relationship("Team")  # Backref is "userteam"

    def __repr__(self):
        """Provide useful output when printing."""

        return "<UT_ID: {ut_id}  User: {user_id}  Team: {team_id}>".format(
            ut_id=self.ut_id, user=self.user_id, team=self.team_id)


class Board(db.Model):
    """Board model"""

    __tablename__ = "boards"

    b_id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                     nullable=False, unique=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team_accounts.t_id'),
                        nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=False)
    desc = db.Column(db.String(255), nullable=True, unique=False)
    updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
        # What does defaul=datetime.utcnow do?

    team = db.relationship("Team")  # Backref is "board"  # Returns ONE thing
    #  num projects? This can be calculated....

    ############ Board - project relationship needs work ##############
    # project = db.relationship("Project")  # Backref is "board"

    def __repr__(self):
        """Provide useful output when printing."""

        return "<B_ID: {b_id}  Name: {name}  Team: {team_id}>".format(
            b_id=self.b_id, name=self.name, team=self.team_id)

# class Project(db.Model):
#     """Project model"""

#     __tablename__ = "projects"

#     p_id = db.Column(db.Integer, primary_key=True, autoincrement=True,
#                      nullable=False, unique=True)
#     board_id = db.Column(db.Integer,
#                          db.ForeignKey('boards.b_id'),
#                          nullable=False)
#     name = db.Column(db.String(100), nullable=False, unique=False)
#     notes = db.Column(db.String(1000), nullable=True, unique=False)
#     # author_id = db.Column(db.String(30),
#                           # db.ForeignKey('user_accounts.u_id'),
#                           # nullable=False, unique=False)
#     claimer_id = db.Column(db.String(30),
#                            db.ForeignKey('user_accounts.u_id'),
#                            nullable=True, unique=False, default=None)
#     upvotes = db.Column(db.Integer, nullable=False, default=0)
#     updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#         # Copied this default expression from flask sqlalchemy docs...
#         # needs more understanding

#     ###### project - board relationship needs work ###################
#     # board = db.relationship("Board")  # Backref is "project"

#     ###### User - projects relationship needs work ###################
#     # author = db.relationship("User")  # Backref is "authored_project"  # This refers to the author...can it be called author????
#     # claimer = db.relationship("User")  # Backref is "claimed_project"  # This can't work...how can the relationship be unique?


#     def __repr__(self):
#         """Provide useful output when printing."""
#         pass
#         # return "<Employee id=%d name=%s>" % (self.id, self.name)


# class Phase(db.Model):
#     """Phase model"""

#     __tablename__ = "phases"

#     phase_id = db.Column(db.Integer, primary_key=True, autoincrement=True,
#                          nullable=False, unique=True)
#     phase_code = db.Column(db.String(10), nullable=False, unique=False)
#     project_id = db.Column(db.Integer, db.ForeignKey('projects.p_id'),
#                            nullable=False)
#     name = db.Column(db.String(100), nullable=False, unique=False)
#     notes = db.Column(db.String(1000), nullable=True, unique=False)
#     updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#         # Copied this default expression from flask sqlalchemy docs...
#         # needs more understanding

#     board = db.relationship("Board", backref="project")

#     def __repr__(self):
#         """Provide useful output when printing."""
#         pass
#         # return "<Employee id=%d name=%s>" % (self.id, self.name)


###################################################################

def connect_to_db(app, db_uri='postgresql:///project'):
    """Connect the database, project, to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = app
    db.init_app(app)


def test_data():
    """Creates data for testing."""

    User.query.delete()
    # Team.query.delete()
    # UserTeam.query.delete()
    # Board.query.delete()

    dany = User(u_id=1, email='dragonvengeance@gmail.com',
                password='Dragonz4life',
                displayname='Dany')
    arya = User(u_id=2, email='ilikewolves@gmail.com',
                password='imissS@ns@',
                displayname='Horseface')
    jon = User(u_id=3, email='broodingallday@hotmail.com',
               password='iknownoth1ng',
               displayname='Jon')
    cersei = User(u_id=4, email='differentinbooks@kingslanding.com',
                  password='JaimeJaime4ev3r',
                  displayname='Queen Cersei')

    # t1 = Team(name='Winterfell', desc='Planning with the Starks')
    # t2 = Team(name="King's Landing", desc='That Lannister Life')
    # t3 = Team(name="Targaryen Queen", desc='Ruling from Essos to Westeros')
    # No userteam relationships yet
    # No boards made yet

    db.session.add_all([dany, arya, jon, cersei])
    db.session.commit()


# def set_user_id_value_after_seed():
#     """After test_data seeds, determines the user id start for
#        serial increment (for dynamic user adds)."""

#     max_u_id = db.session.query(func.max(User.u_id)).one()
#         # returns a single value tuple >>> (int,)
#     max_u_id


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)

    db.create_all()
    # test_data()   ##### UNCOMMENT WHEN YOU WANT TO RESEED
    # set_user_id_value_after_seed()
    print "Connected to DB."
