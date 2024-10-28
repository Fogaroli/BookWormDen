import os
import sys
import pytest
from flask import session

# Setup relative path in order to import the flask application modules:
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from models import connect_db, db, User, Book, UserBook

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
def client():
    """Cliente test client for http requests"""
    return app.test_client()


@pytest.fixture
def test_user(context):
    """Create a test user"""
    u1 = User.signup(
        {
            "email": "test1@test.com",
            "username": "testuser1",
            "password": "PassWord1",
            "first_name": "Test User",
            "last_name": "Number 1",
        }
    )
    return u1


def test_homepage(context, test_user, client):
    """Test homepage route."""
    resp = client.get("/")
    assert resp.status_code == 200
    assert "Welcome to the Book Worm Den" in str(resp.data)

    with client.session_transaction() as sess:
        sess["CURRENT_USER"] = test_user.id

    resp = client.get("/")
    assert resp.status_code == 200
    assert test_user.username in str(resp.data)


def test_signup(client):
    """Test user signup."""
    resp = client.get("/register")
    assert resp.status_code == 200
    assert "Join the Den" in str(resp.data)
    assert "E-mail" in str(resp.data)

    resp = client.post(
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
    assert resp.status_code == 200
    assert "My Name 2" in str(resp.data)


def test_login(context, test_user, client):
    """Test user login route."""
    resp = client.get("/login")
    assert resp.status_code == 200
    assert "Username" in str(resp.data)

    resp = client.post(
        "/login",
        data={"username": "testuser1", "password": "PassWord1"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert "testuser1" in str(resp.data)

    with client.session_transaction() as sess:
        assert "CURRENT_USER" in sess
        assert sess["CURRENT_USER"] == test_user.id


def test_logout(context, test_user, client):
    """Test user logout."""
    with client.session_transaction() as sess:
        sess["CURRENT_USER"] = test_user.id

    resp = client.post("/logout", follow_redirects=True)
    assert resp.status_code == 200
    assert "Sign-Up" in str(resp.data)

    with client.session_transaction() as sess:
        assert "CURRENT_USER" not in sess


def test_invalid_login(context, test_user, client):
    """Test login with invalid credentials"""
    resp = client.post(
        "/login", data={"username": "testuser2", "password": "wrongpassword"}
    )
    assert "User and/or password invalid" in str(resp.data)


def test_user_page(context, test_user, client):
    """Test user home route."""
    resp = client.get("/user", follow_redirects=True)
    assert resp.status_code == 200
    assert "Please login first" in str(resp.data)

    with client.session_transaction() as sess:
        sess["CURRENT_USER"] = test_user.id

    resp = client.get("/user")
    assert resp.status_code == 200
    assert test_user.first_name in str(resp.data)
    assert "This page is not visible by any other user" in str(resp.data)
