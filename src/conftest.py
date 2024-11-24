import os
import pytest
from models import (
    connect_db,
    db,
    User,
    Book,
    UserBook,
    Comment,
    Club,
    ClubBook,
    ClubMembers,
    Message,
)

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


@pytest.fixture(scope="session")
def models():
    """Expose all models to tests."""
    return {
        "User": User,
        "Book": Book,
        "UserBook": UserBook,
        "Comment": Comment,
        "Club": Club,
        "ClubBook": ClubBook,
        "ClubMembers": ClubMembers,
        "Message": Message,
    }


@pytest.fixture()
def context():
    """Create an app context."""
    with app.app_context() as context:
        context.push()
        db.drop_all()
        db.create_all()
        yield
        db.session.rollback()
        db.drop_all()
        context.pop()


@pytest.fixture()
def client(context):
    """Cliente test client for http requests"""
    return app.test_client()


@pytest.fixture
def test_user(context, models):
    """Create a test user"""
    u1 = models["User"].signup(
        {
            "email": "test1@test.com",
            "username": "testuser1",
            "password": "PassWord1",
            "first_name": "Test User",
            "last_name": "Number 1",
        }
    )
    db.session.commit()
    return u1


@pytest.fixture
def test_book(context, models):
    """Create a test book."""
    book = models["Book"].save_book(
        {
            "api_id": "-abc123",
            "title": "Test Book",
            "cover": "https://example.com/cover.jpg",
        }
    )
    db.session.commit()
    return book
