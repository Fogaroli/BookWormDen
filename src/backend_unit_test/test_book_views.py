import os
import sys
from unittest import TestCase

# Setup relative path in order to import the flask application modules:
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

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


class BookSeachTestCase(TestCase):
    """Test API for book search, which interacts with google books API."""

    def setUp(self):
        """Create test client."""
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()

    def tearDown(self):
        self.app_context.pop()
        return

    def test_search(self):
        """Test book search by title."""
        with self.client as c:
            resp = c.get("/search?q=Harry+Potter")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Harry Potter", str(resp.json))
            self.assertTrue(
                {"title", "authors", "description", "thumbnail"}.issubset(
                    resp.json[0]["data"].keys()
                )
            )
            self.assertLess(10, len(resp.json))

    def test_book_details(self):
        """Test route to collect book details"""
        ### Using Ids JHEkAQAAMAAJ and kpnHBAAAQBAJ collected during develop using the search above.
        ### Google BOOKs volume ids are permanent descriptors of each volume.
        with self.client as c:
            resp = c.get("/book/kpnHBAAAQBAJ")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Harry Potter and the Order of the Phoenix", str(resp.json))
            self.assertTrue(
                {
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
            )
