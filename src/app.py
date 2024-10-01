"""
================================================================
Title: Book Worm Den
Author: Fabricio Ribeiro
Date: September 17, 2024

================================================================
"""

import os
from flask import Flask, flash, render_template, redirect, session, g, url_for, request
from functools import wraps
from flask_debugtoolbar import DebugToolbarExtension
from dotenv import load_dotenv
from models import db, connect_db, User
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
Supporting functions
"""


def login_required(f):
    """Decorator function to control protected views"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "CURRENT_USER" not in session:
            flash("Please login first", "danger")
            return redirect(url_for("login_view", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


def login(user):
    """Function to process login, store user information on flask session"""
    session["CURRENT_USER"] = user.id


def logout():
    """Function to process logout, remove user information from flask session"""
    session.pop("CURRENT_USER")


@app.before_request
def load_user():
    """If user login id found in session, load current user to Flask global."""

    if "CURRENT_USER" in session:
        g.user = db.get_or_404(User, session["CURRENT_USER"])

    else:
        g.user = None


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


@app.route("/register", methods=["GET", "POST"])
def registration_view():
    """View function for new user registration"""

    registration_form = UserAddForm()
    if registration_form.validate_on_submit():
        new_user = User.signup(registration_form.data)
        if new_user:
            flash(f"Welcome {new_user.first_name} to the BookWormDen", "success")
            login(new_user)
            return redirect(url_for("homepage"))
        else:
            flash(f"Error creating new user, please try again", "danger")

    return render_template("user_signup.html", form=registration_form)


@app.route("/login", methods=["GET", "POST"])
def login_view():
    """View function for user login"""
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_attempt = (
            db.session.query(User)
            .filter(User.username == login_form.data["username"])
            .first()
        )
        if user_attempt and user_attempt.validate_user(login_form.data["password"]):
            login(user_attempt)
            flash(f"Welcome back {user_attempt.first_name}", "success")
            return redirect(url_for("user_page"))
        else:
            flash("User and/or password invalid, please try again", "danger")
    return render_template("user_login.html", form=login_form)


@app.route("/logout", methods=["POST"])
def logout_view():
    """View function for user logout"""
    if g.user:
        logout()
    return redirect(url_for("homepage"))


@app.route("/user")
@login_required
def user_page():
    """View function to open user homepage"""
    return render_template("user_page.html")
