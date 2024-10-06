"""
================================================================
Title: Book Worm Den
Author: Fabricio Ribeiro
Date: September 17, 2024

================================================================
"""

import os
from flask import (
    Flask,
    flash,
    render_template,
    redirect,
    session,
    g,
    url_for,
    request,
    jsonify,
)
from functools import wraps
from flask_debugtoolbar import DebugToolbarExtension
from dotenv import load_dotenv
from models import db, connect_db, User
from forms import UserAddForm, LoginForm
import requests

# Load environmental variables file
load_dotenv()

# Import Environmental Variables
production_db = os.environ.get(
    "DB_URI"
)  # If local database should have the format: "postgresql:///<dbname>"
testrun = os.environ.get("TESTRUN")  # True or False
secret_code = os.environ.get("SECRETE_KEY")
api_key = os.environ.get("GOOGLE_API_KEY")

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


# Setup Google API
GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"


"""
# Supporting functions
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
# View functions
"""

"""
User registration and login
"""


@app.route("/", methods=["GET"])
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
            flash("Error creating new user, please try again", "danger")

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


@app.route("/user", methods=["GET"])
@login_required
def user_page():
    """View function to open user homepage"""
    return render_template("user_page.html")


"""
Book search engine
"""


@app.route("/search", methods=["GET"])
def search_books():
    title_search = request.args.get("q")
    if not title_search:
        return jsonify({"error": "Please enter a book title to search"}), 400

    params = {
        "q": f"intitle:{title_search}",
        "key": api_key,
        "maxResults": 40,
        "printType": "books",
        # "projection": "lite",
        "langRestrict": "en",
    }

    response = requests.get(url=GOOGLE_BOOKS_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        books = {}
        for item in data.get("items", []):
            if item["volumeInfo"]["language"] == "en":
                id = item.get("id")
                books[id] = []
                volume_info = item.get(
                    "volumeInfo", {}
                )  # volume is the google book term for an item (book, magazine or other content)
                books[id].append(
                    {
                        "title": volume_info.get("title"),
                        "authors": volume_info.get("authors", []),
                        "publishedDate": volume_info.get("publishedDate"),
                        "description": volume_info.get("description"),
                        "thumbnail": volume_info.get("imageLinks", {}).get("thumbnail"),
                        "id": volume_info.get("id"),
                    }
                )
        return jsonify(books)
    else:
        return jsonify(
            {"error": "Failed to fetch data please try again"}
        ), response.status_code


@app.route("/book/<id>", methods=["GET"])
def get_book_details(id):
    params = {
        "key": api_key,
    }

    response = requests.get(url=f"{GOOGLE_BOOKS_API_URL}/{id}", params=params)
    if response.status_code == 200:
        data = response.json()
        book_data = []
        volume_info = data.get(
            "volumeInfo", {}
        )  # volume is the google book term for an item (book, magazine or other content)
        book_data.append(
            {
                "title": volume_info.get("title"),
                "authors": volume_info.get("authors", []),
                "categories": volume_info.get("categories", []),
                "publisher": volume_info.get("publisher"),
                "publishedDate": volume_info.get("publishedDate"),
                "description": volume_info.get("description"),
                "thumbnail": volume_info.get("imageLinks", {}).get("thumbnail"),
                "page_count": volume_info.get("PageCount"),
                "average_rating": volume_info.get("averageRating"),
            }
        )
        return jsonify(book_data)
    else:
        return jsonify(
            {"error": "Failed to fetch data please try again"}
        ), response.status_code
