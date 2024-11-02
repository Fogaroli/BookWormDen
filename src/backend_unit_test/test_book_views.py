import os
import sys
import pytest

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


@pytest.fixture
def test_book(context):
    """Create a test book."""
    book = Book.saveBook({"api_id": "-abc123", "title": "Test Book"})
    return book


def test_search(client):
    """Test book search by title."""
    resp = client.get("/search?q=Harry+Potter")
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert "Harry Potter" in str(resp.json)
    assert {"title", "authors", "description", "thumbnail"}.issubset(
        resp.json[0]["data"].keys()
    )
    assert 10 < len(resp.json)


def test_invalid_book_search(context, client):
    """Test book search with invalid query."""
    resp = client.get("/search?q=")
    assert resp.status_code == 400
    assert "Please enter a book title to search" in str(resp.json)


def test_book_details(client):
    """Test route to collect book details"""
    ### Using Ids JHEkAQAAMAAJ and kpnHBAAAQBAJ collected during develop using the search above.
    ### Google BOOKs volume ids are permanent descriptors of each volume.
    resp = client.get("/book/kpnHBAAAQBAJ")
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert "Harry Potter and the Order of the Phoenix" in str(resp.json)
    assert {
        "title",
        "authors",
        "categories",
        "publisher",
        "publishedDate",
        "page_count",
        "average_rating",
        "description",
        "thumbnail",
    }.issubset(resp.json.keys())


def test_add_book_to_user(client, context, test_user, test_book):
    """Test adding book to user's reading list."""
    resp = client.post(
        "/login",
        data={"username": "testuser1", "password": "PassWord1"},
        follow_redirects=True,
    )
    assert "testuser1" in str(resp.data)

    resp = client.post(
        f"/book/{test_book.api_id}/add-to-user",
        data={"book_title": test_book.title},
        follow_redirects=True,
    )

    assert resp.status_code == 200
    assert test_book in test_user.books
    assert test_book.title in str(resp.data)


def test_user_book_status(context, test_user, test_book):
    """Test UserBook relationship and status."""
    user_book = UserBook(
        user_id=test_user.id,
        book_id=test_book.api_id,
    )
    db.session.add(user_book)
    db.session.commit()

    assert user_book in test_user.readlog
