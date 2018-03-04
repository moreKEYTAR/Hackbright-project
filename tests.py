"""Tests require use of testdb; make sure to make this empty database before
    running this file."""

import unittest
from server import app
from model import (db, connect_to_db,
                   User, Team, UserTeam, Board, Project, Phase)
import seed
import query  # no tests yet
import helper  # no tests yet
from flask import session


# class FlaskMakeUser(unittest.TestCase):
#     """Test log in and log out."""

#     def setUp(self):
#         """Code to run before every test."""

#         app.config['TESTING'] = True
#         # app.config['SECRET_KEY'] = app.secret_key
#         self.client = app.test_client()
# class modelTests(unittest.TestCase):
#     """Tests for the data ORM in model.py."""
#     pass
#     # def setUp(self):
#     #     """Code to run before every test."""

#     #     self.client = model.app.test_client()

#     #     model.app.config['TESTING'] = True

###########################################################################
# INDEX ###################################################################

class FlaskBasicTests(unittest.TestCase):
    """Tests for the site routes loading, content in server.py."""

    def setUp(self):
        """Code to run before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
        """Can we reach the homepage?"""

        result = self.client.get("/")
        self.assertIn("Welcome", result.data)


###########################################################################
# REGISTRATION ############################################################

class DatabaseTests(unittest.TestCase):
    """Tests for adding/updating an empty db; usess session and queries."""

    def setUp(self):
        """Code to run before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///testdb")
        db.create_all()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_make_new_user(self):
        """Test making new user."""

        with self.client as c:  # required for using session
            result = c.post("/users/new",
                            data={"email": "testing@gmail.com", "pw": "123abc"},
                            follow_redirects=True)

            self.assertIn("Dashboard", result.data)
            self.assertEqual(session["new_user"], True)
            self.assertEqual(session["login"], True)

# ----------------------------------------------------------------------
# Traceback (most recent call last):
#   File "tests.py", line 81, in test_make_new_user
#     self.assertIn("Dashboard", result.data)
# AssertionError: 'Dashboard' not found in '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>404 Not Found</title>\n<h1>Not Found</h1>\n<p>The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.</p>\n'


    def test_query_for_created_user(self):
        """Test for finding user just created."""

        user_record = User.query.filter(User.email == "testing@gmail.com"
                                        ).first()
        self.assertEqual(user_record.password == "123abc")

# Traceback (most recent call last):
#   File "tests.py", line 90, in test_query_for_created_user
#     self.assertEqual(user_record.password == "123abc")
# AttributeError: 'NoneType' object has no attribute 'password'


###########################################################################
# LOG IN ##################################################################


###########################################################################
# DASHBOARD ###############################################################


###########################################################################
# TEAM VIEW ###############################################################


###########################################################################
# LOG OUT #################################################################


###########################################################################
# SEEDED DATABASE #########################################################

class DatabaseSeedTests(unittest.TestCase):
    """Tests for seeded data, using queries."""

    def setUp(self):
        """Code to run before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        seed.load_users()
        seed.load_teams()
        seed.load_userteams()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_login(self):
        """Test login route with testdb user data."""

        result = self.client.post("/users/login",
                                  data={"email": "summerchild@gmail.com",
                                        "pw": "wolfdreams"},
                                  follow_redirects=True)
        self.assertIn("Dashboard", result.data)

# Traceback (most recent call last):
#   File "tests.py", line 140, in test_login
#     self.assertIn("Dashboard", result.data)
# AssertionError: 'Dashboard' not found in '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>404 Not Found</title>\n<h1>Not Found</h1>\n<p>The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.</p>\n'

###########################################################################
# SEEDED DATABASE #########################################################

class DatetimeTests(unittest.TestCase):
    """Tests for the site routes loading, content in server.py."""

    def setUp(self):
        """Code to run before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_count_projects_fn(self):
        """Does the fn return the correct list of integers?"""
        import datetime
        self.assertEqual(helper.count_projects_per_day(
                            [datetime.datetime(2018, 2, 26, 22, 13, 42, 698510),
                            datetime.datetime(2018, 2, 26, 22, 13, 42, 698510),
                            datetime.datetime(2018, 2, 26, 22, 13, 42, 698510),
                            datetime.datetime(2018, 2, 27, 14, 13, 42, 698510),
                            datetime.datetime(2018, 2, 27, 14, 13, 42, 698510),
                            datetime.datetime(2018, 2, 27, 14, 13, 42, 698510),
                            datetime.datetime(2018, 2, 27, 14, 13, 42, 698510),
                            datetime.datetime(2018, 2, 28, 22, 13, 42, 698510),
                            datetime.datetime(2018, 2, 28, 22, 13, 42, 698510),
                            datetime.datetime(2018, 3, 1, 22, 13, 42, 698510),
                            datetime.datetime(2018, 3, 1, 22, 13, 42, 698510),
                            datetime.datetime(2018, 3, 1, 22, 13, 42, 698510),
                            datetime.datetime(2018, 3, 1, 22, 13, 42, 698510),
                            datetime.datetime(2018, 3, 2, 17, 13, 42, 698510),
                            datetime.datetime(2018, 3, 2, 17, 13, 42, 698510),
                            datetime.datetime(2018, 3, 2, 17, 13, 42, 698510),
                            datetime.datetime(2018, 3, 2, 17, 13, 42, 698510),
                            datetime.datetime(2018, 3, 2, 17, 13, 42, 698510),
                            datetime.datetime(2018, 3, 2, 17, 13, 42, 698510),
                            datetime.datetime(2018, 3, 3, 22, 13, 42, 698510),
                            datetime.datetime(2018, 3, 3, 22, 13, 42, 698510)],
                        datetime.datetime(2018, 2, 26, 12, 13, 42, 698510),
                        6),
                        [2, 6, 4, 2, 4, 3])
        # >>> start = (datetime.datetime(2018, 2, 26, 12, 13, 42, 698510))
        # >>> total_days = 6
        # >>> count_projects_per_day(lst, start, total_days)
        # [2, 6, 4, 2, 4, 3]



###########################################################################
# DIRECT FILE CALL ########################################################

if __name__ == "__main__":

    unittest.main()
