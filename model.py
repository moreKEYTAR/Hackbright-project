"""Models and database functions for database called project."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# import query  # Added this to access query functions...implementation TBD.

db = SQLAlchemy()


######################################################################
######################################################################

class User(db.Model):
    """User model"""

    __tablename__ = "user_accounts"

    u_id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                     nullable=False, unique=True)
    email = db.Column(db.String(254), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=True, unique=False)
        # Nullable for when a user has not registered. Required at user registration, however.
        # password_salt = db.Column(db.String(50), nullable=False)
        # password_hash_algorithm = db.Column(db.String(50), nullable=False)
    displayname = db.Column(db.String(30), nullable=False, unique=False)
    is_registered = db.Column(db.Boolean, nullable=False, default=True)

    # SEE UserTeam FOR RELATIONSHIP
    # SEE Project FOR RELATIONSHIP

    def __repr__(self):
        """Provide useful output when printing: User."""
        return "<{email}  U_ID: {u_id}  Displayname: {display}>".format(
            email=self.email, u_id=self.u_id, display=self.displayname)


class Team(db.Model):
    """Team model"""

    __tablename__ = "team_accounts"

    t_id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                     nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False, unique=False)
    desc = db.Column(db.String(255), nullable=True, unique=False)

    # SEE UserTeam FOR RELATIONSHIP
    # SEE Board FOR RELATIONSHIP

    def __repr__(self):
        """Provide useful output when printing: Team."""
        return "<{name}  T_ID: {t_id}>".format(name=self.name, t_id=self.t_id)


class UserTeam(db.Model):
    """UserTeam model, with is_member status"""

    __tablename__ = "users_teams"

    ut_id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                      nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_accounts.u_id'),
                        nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team_accounts.t_id'),
                        nullable=False)
    is_member = db.Column(db.Boolean, nullable=True)
        # True if accepted member (started team, etc)
        # False if declined invitation
        # Null if invited and no decision yet

    user = db.relationship("User", backref="userteams")
    team = db.relationship("Team", backref="userteams")

    def __repr__(self):
        """Provide useful output when printing."""
        return "<UT_ID: {ut_id}  User: {user}  Team: {team}>".format(
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

    team = db.relationship("Team", backref="boards")
    # SEE Project FOR RELATIONSHIP

    def __repr__(self):
        """Provide useful output when printing."""
        return "<B_ID: {b_id}  Name: {name}  Team: {team}>".format(
            b_id=self.b_id, name=self.name, team=self.team_id)


class Project(db.Model):
    """Project model"""

    __tablename__ = "projects"

    p_id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                     nullable=False, unique=True)
    board_id = db.Column(db.Integer,
                         db.ForeignKey('boards.b_id'),
                         nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user_accounts.u_id'),
                        nullable=True, unique=False, default=None)
    phase_code = db.Column(db.String(10),
                           db.ForeignKey('phases.ph_code'),
                           nullable=False, unique=False)
    title = db.Column(db.String(300), nullable=False, unique=False)
    notes = db.Column(db.String(2000), nullable=True, unique=False)
    upvotes = db.Column(db.Integer, nullable=True, default=1)
    updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
        # needs more study

    board = db.relationship("Board", backref="projects")
    user = db.relationship("User", backref="projects")
    phase = db.relationship("Phase", backref="projects")

    def __repr__(self):
        """Provide useful output when printing."""
        return """<{p_id}  Title: {title}  Type: {phase}
        Claimed by: {user} Board: {board}>""".format(
            p_id=self.p_id,
            title=self.title,
            phase=self.phase_code,
            user=self.user_id,
            board=self.board_id)


class Phase(db.Model):
    """Phase model"""

    __tablename__ = "phases"

    ph_code = db.Column(db.String(10), primary_key=True,
                        nullable=False, unique=True)
    # SEE Project FOR RELATIONSHIP

    def __repr__(self):
        """Provide useful output when printing."""
        return "<{}>".format(self.ph_code)


######################################################################
######################################################################

def connect_to_db(app, db_uri='postgresql:///project'):
    """Connect the database, project, to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = app
    db.init_app(app)


######################################################################
######################################################################

if __name__ == "__main__":

    from server import app
    # As a convenience, if we run this module interactively, it will leave
        # you in a state of being able to work with the database directly.
    connect_to_db(app)
    print "Connected to DB."
