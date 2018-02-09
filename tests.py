import unittest
from server import app
from model import db, connect_to_db, User, Team, UserTeam, Board
from flask import session
import seed
import os


class FlaskBasicTests(unittest.TestCase):
    """Tests for the site routes loading, content in server.py."""

    def setUp(self):
        """Code to run before every test."""

        self.client = app.test_client()
            # Use Balloonicorn Flask app lab; replaced "party" with "server"
        app.config['TESTING'] = True

    def test_index(self):
        """Can we reach the homepage?"""

        result = self.client.get("/")
        self.assertIn("Welcome", result.data)


# class FlaskMakeUser(unittest.TestCase):
#     """Test log in and log out."""

#     def setUp(self):
#         """Code to run before every test."""

#         app.config['TESTING'] = True
#         # app.config['SECRET_KEY'] = app.secret_key
#         self.client = app.test_client()


class DatabaseSeedTests(unittest.TestCase):
    """Tests for seeded data, using queries."""

    def setUp(self):
        """Code to run before every test."""

        self.client = app.test_client()
            # Use Balloonicorn Flask app lab; replaced "party" with "server"
        app.config['TESTING'] = True

        # os.system('dropdb testdb')
        # os.system('createdb testdb')
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        seed.load_users()
        seed.load_teams()
        seed.load_userteams()
        seed.set_user_id_value_after_seed()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()
        # os.system('dropdb testdb')

    def test_login(self):
        """Test login route with testdb user data."""

        result = self.client.post("/users/login",
                                  data={"email": "summerchild@gmail.com",
                                        "pw": "wolfdreams"},
                                  follow_redirects=True)
        self.assertIn("Dashboard", result.data)

    def test_make_new_user(self):
        """Test making new user."""

        with self.client as c:  # required for using session
            result = c.post("/users/new", data={"email": "testing@gmail.com",
                                                "pw": "123abc"},
                            follow_redirects=True)

            self.assertIn("Dashboard", result.data)
            self.assertEqual(session["new_user"], True)
            self.assertEqual(session["login"], True)

    def query_for_created_user(self):
        """Test for finding user just created."""

        user_record = User.query.filter(User.email == "testing@gmail.com").first()
        self.assertEqual(user_record.password == "123abc")


class modelTests(unittest.TestCase):
    """Tests for the data ORM in model.py."""
    pass
    # def setUp(self):
    #     """Code to run before every test."""

    #     self.client = model.app.test_client()

    #     model.app.config['TESTING'] = True

if __name__ == "__main__":

    unittest.main()
