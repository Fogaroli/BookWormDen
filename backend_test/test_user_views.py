import os
import sys
from unittest import TestCase

# Setup relative path in order to import the flask application modules:
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from models import connect_db, db, User

# BEFORE we import our app, let's set an environmental variable
# to identify it is a test run. It will prevent connecting to
# production database, so we can redirect to a test database
# and connect to it.

os.environ["TESTRUN"] = "True"

# Now we can import app
from app import app


app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("TEST_DB_URI")
app.config["SQLALCHEMY_ECHO"] = False
app.config["WTF_CSRF_ENABLED"] = False
connect_db(app)


class UserViewTestCase(TestCase):
    """Test views for user routes."""

    def setUp(self):
        """Create test client, add sample data."""
        self.app_context = app.app_context()
        self.app_context.push()
        User.query.delete()

        self.client = app.test_client()

        self.u1 = User.signup(
            {
                "username": "testuser1",
                "password": "PassWord1",
                "email": "test1@test.com",
                "first_name": "My Name",
                "last_name": "surname",
            }
        )

    def tearDown(self):
        self.app_context.pop()
        return

    def test_homepage(self):
        """Test homepage route."""
        with self.client as c:
            resp = c.get("/")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Welcome to the Book Worm Den", str(resp.data))

        with self.client as c:
            with c.session_transaction() as sess:
                sess["CURRENT_USER"] = self.u1.id

            resp = c.get("/")

            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.u1.username, str(resp.data))

    def test_signup(self):
        """Test user signup."""
        with self.client as c:
            resp = c.get("/register")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Join the Den", str(resp.data))
            self.assertIn("E-mail", str(resp.data))

        with self.client as c:
            resp = c.post(
                "/register",
                data={
                    "username": "testuser2",
                    "email": "test2@test.com",
                    "password": "password",
                    "first_name": "My Name 2",
                    "last_name": "surname 2",
                },
                follow_redirects=True,
            )
            self.assertEqual(resp.status_code, 200)
            self.assertIn("My Name 2", str(resp.data))

    def test_login(self):
        """Test user login route."""
        with self.client as c:
            resp = c.get("/login")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Username", str(resp.data))

        with self.client as c:
            resp = c.post(
                "/login",
                data={"username": "testuser2", "password": "password"},
                follow_redirects=True,
            )
            self.assertEqual(resp.status_code, 200)
            self.assertIn("testuser2", str(resp.data))

    def test_logout(self):
        """Test user logout."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess["CURRENT_USER"] = self.u1.id

            resp = c.post("/logout", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Sign-Up", str(resp.data))

            with c.session_transaction() as sess:
                self.assertIsNone(sess.get("CURRENT_USER"))

    def test_user_page(self):
        """Test user home route."""
        with self.client as c:
            with c.session_transaction() as sess:
                sess["CURRENT_USER"] = self.u1.id

            resp = c.get("/user")
            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.u1.first_name, str(resp.data))
            self.assertIn("This page is not visible by any other user", str(resp.data))
