"""
================================================================    
Title: Book Worm Den
Author: Fabricio Ribeiro
Date: September 17, 2024

================================================================
"""

import os
from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from dotenv import load_dotenv
from models import connect_db

# Load environmental variables file
load_dotenv()

# Import Environmental Variables
production_db = os.environ.get("DB_URI") # If local database should have the format: "postgresql:///<dbname>"
testrun = os.environ.get("TESTRUN") # True or False
secret_code = os.environ.get("SECRETE_KEY")

# Setup Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = secret_code
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
debug = DebugToolbarExtension(app)

# Detect if testing environmental variable is set to True
if not testrun:
    app.config["SQLALCHEMY_DATABASE_URI"] = production_db
    connect_db(app)

# In case of running the app on python terminal
if __name__ == "__main__":
    app.app_context().push()


"""
View functions
"""


@app.route("/")
def homepage():
    """View Function for the portal homepage.

    Actions:
    
    Returns:
        Render Homepage template file
    """
    return render_template("homepage.html")
