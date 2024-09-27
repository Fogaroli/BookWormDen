import os
import sys
from unittest import TestCase

# Setup relative path in order to import the flask application modules:
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from models import connect_db

# BEFORE we import our app, let's set an environmental variable
# to identify it is a test run. It will prevent connecting to
# production database, so we can redirect to a test database
# and connect to it.

os.environ["TESTRUN"] = True

# Now we can import app
from app import app


app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("TEST_DB_URI")
app.config["SQLALCHEMY_ECHO"] = False
connect_db(app)


# Tests goes here
