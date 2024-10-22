import os
import sys
from unittest import TestCase

# Setup relative path in order to import the flask application modules:
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from models import db, connect_db, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database


os.environ["TESTRUN"] = "True"

# Now we can import app
from app import app

# Database connection is not established inside the flask app since the TESTRUN flag is enabled.

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["TEST_DB_URI"]
app.config["SQLALCHEMY_ECHO"] = False
connect_db(app)


class UserModelTestCase(TestCase):
    """Test user database model."""

    def setUp(self):
        """
        Function to create the environment before every test.
        Drops and Creates the tables on the database
        Create test app context
        Add sample data."""

        self.app_context = app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

        self.u1 = User(
            email="test1@test.com",
            username="testuser1",
            password="PassWord1",
            first_name="Test User",
            last_name="Number 1",
        )

    def tearDown(self):
        """
        Function to tear down data created for each test function.
        End the test app context.
        """
        self.app_context.pop()
        return

    def test_user_model(self):
        """Does basic model work?"""

        db.session.add(self.u1)
        db.session.commit()

        self.assertIsNotNone(self.u1.id)
        self.u1.image_url = "image_test"
        self.u1.bio = "this is a bio"
        self.u1.location = "location test"
        db.session.commit()
        self.assertEqual(self.u1.image_url, "image_test")
        self.assertEqual(self.u1.bio, "this is a bio")
        self.assertEqual(self.u1.location, "location test")

    def test_user_sign_up(self):
        """Check if the class method to register a new user is working"""

        new_user = User.signup(
            {
                "username": "testuser5",
                "password": "PassWord5",
                "email": "test5@test.com",
                "first_name": "My Name",
                "last_name": "surname",
            }
        )

        self.assertIsNotNone(new_user.id)

        self.assertTrue(new_user)
        db.session.add(self.u1)
        db.session.commit()

        new_user2 = User.signup(
            {
                "username": "testuser1",
                "password": "PassWord6",
                "email": "test6@test.com",
                "first_name": "My Name 6",
                "last_name": "surname",
            }
        )
        self.assertFalse(new_user2)

        new_user3 = User.signup(
            {
                "username": "testuser7",
                "password": "PassWord7",
                "email": "test1@test.com",
                "first_name": "My Name 7",
                "last_name": "surname",
            }
        )
        self.assertFalse(new_user3)

    def test_user_authentication(self):
        """Check if the class method to authentication the user is working as expected"""

        new_user = User.signup(
            {
                "username": "testuser5",
                "password": "PassWord5",
                "email": "test5@test.com",
                "first_name": "My Name",
                "last_name": "surname",
            }
        )

        self.assertNotEqual(new_user.password, "PassWord5")

        self.assertTrue(new_user.validate_user("PassWord5"))

        self.assertFalse(new_user.validate_user("PassWord"))
