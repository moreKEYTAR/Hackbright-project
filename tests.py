import unittest
import server
# import model
# import query  # no class yet


class serverTests(unittest.TestCase):
    """Tests for the site routes loading, content in server.py."""

    def setUp(self):
        """Code to run before every test."""

        self.client = server.app.test_client()
            # Use Balloonicorn Flask app lab; replaced "party" with "server"
        server.app.config['TESTING'] = True

    def test_index(self):
        """Can we reach the homepage?"""

        result = self.client.get("/")
        self.assertIn("Welcome", result.data)

    def test_2(self):
        """????"""
        pass

    def test_3(self):
        """????"""

        pass

    def test_4(self):
        """????"""

        pass


class modelTests(unittest.TestCase):
    """Tests for the data ORM in model.py."""

    def setUp(self):
        """Code to run before every test."""

        self.client = model.app.test_client()
            # Use Balloonicorn Flask app lab; replaced "party" with "model"
        model.app.config['TESTING'] = True

if __name__ == "__main__":
    unittest.main()

