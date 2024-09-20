# run these tests like:
#
#    python -m unittest test_app.py

import os
from unittest import TestCase
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from models import connect_db

load_dotenv()

# BEFORE we import our app, let's set an environmental variable
# to identify it is a test run. It will prevent connecting to 
# production database, so we can redirect to a test database
# and connect to it.

os.environ["TESTRUN"] = True

# Now we can import app
from app import app

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("TEST_DB_URI")
connect_db(app)


# Tests goes here