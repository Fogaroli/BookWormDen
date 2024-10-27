import os
import sys
import pytest

# Setup relative path in order to import the flask application modules:
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from models import db, connect_db, User, Book, UserBook

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


@pytest.fixture
def context():
    """Create an app context."""
    with app.app_context() as context:
        context.push()
        db.drop_all()
        db.create_all()
        yield
        context.pop()


@pytest.fixture
def test_user(context):
    """Create a test user"""
    u1 = User(
        email="test1@test.com",
        username="testuser1",
        password="PassWord1",
        first_name="Test User",
        last_name="Number 1",
    )
    return u1


@pytest.fixture
def test_book(context):
    """Create a test book"""
    book = Book(api_id="test123", title="Test Book")
    return book


# Database model tests


# User
def test_user_model(context, test_user):
    """Does basic model work?"""

    db.session.add(test_user)
    db.session.commit()

    assert test_user.id is not None

    test_user.image_url = "image_test"
    test_user.bio = "this is a bio"
    test_user.location = "location test"
    db.session.commit()

    assert test_user.image_url == "image_test"
    assert test_user.bio == "this is a bio"
    assert test_user.location == "location test"


def test_user_sign_up(context, test_user):
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

    assert new_user.id is not None

    assert new_user

    db.session.add(test_user)
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
    assert not new_user2

    new_user3 = User.signup(
        {
            "username": "testuser7",
            "password": "PassWord7",
            "email": "test1@test.com",
            "first_name": "My Name 7",
            "last_name": "surname",
        }
    )
    assert not new_user3


def test_user_authentication(context):
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

    assert new_user.password != "PassWord5"
    assert new_user.validate_user("PassWord5")
    assert not new_user.validate_user("PassWord")


# Book
def test_book_model(context, test_book):
    """Test Book model."""

    db.session.add(test_book)
    db.session.commit()

    assert test_book.api_id is not None

    book = Book.saveBook({"api_id": "book123", "title": "Test Book Title"})

    assert book.api_id == "book123"
    assert book.title == "Test Book Title"


def test_user_book_relationship(context, test_user, test_book):
    """Test User-Book relationship."""
    # Add book to user's reading list
    test_user.books.append(test_book)
    db.session.commit()

    # Test relationship
    assert test_book in test_user.books
    assert test_user in test_book.users
