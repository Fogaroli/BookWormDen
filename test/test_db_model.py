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
            password="HASHED_PASSWORD",
            first_name="Test User",
            last_name="Number 1",
        )
        self.u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD",
            first_name="Tester",
            last_name="Number 2",
        )
        self.u3 = User(
            email="test3@test.com",
            username="testuser3",
            password="HASHED_PASSWORD",
            first_name="Testing",
            last_name="User 3",
        )
        self.u4 = User(
            email="test4@test.com",
            username="testuser4",
            password="HASHED_PASSWORD",
            first_name="Test User",
            last_name="Number 4",
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
