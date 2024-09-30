"""
================================================================
Title: Book Worm Den
Author: Fabricio Ribeiro
Date: September 17, 2024

================================================================
"""

import os
from flask import Flask, flash, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from dotenv import load_dotenv
from models import connect_db, User
from forms import UserAddForm, LoginForm

# Load environmental variables file
load_dotenv()

# Import Environmental Variables
production_db = os.environ.get(
    "DB_URI"
)  # If local database should have the format: "postgresql:///<dbname>"
testrun = os.environ.get("TESTRUN")  # True or False
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


def login(user):
    session["CURRENT_USER"] = user.id


@app.route("/")
def homepage():
    """View Function for the portal homepage.

    Actions:

    Returns:
        Render Homepage template file
    """
    return render_template("homepage.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """View function for new user registration"""

    registration_form = UserAddForm()
    if registration_form.validate_on_submit():
        new_user = User.signup(registration_form.data)
        if new_user:
            flash(f"Welcome {new_user.username} to the BookWormDen", "success")
            login(new_user)
            return redirect("/")
        else:
            flash(f"Error creating new user, please try again", "danger")
    else:
        return render_template("user_signup.html", form=registration_form)
