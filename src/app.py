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
from models import db, connect_db, User, Book, UserBook, Comment
from forms import UserAddForm, LoginForm, readStatisticsForm
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
    reading_log = g.user.readlog
    return render_template("user_page.html", list=reading_log)


@app.route("/user/add-book", methods=["POST"])
@login_required
def addBookToUserList():
    """Function to add a volume to the user reading list.
    If the book does not exist in the local dictionary, this function will add it before adding to the user reading list.
    """
    book_entry = db.session.get(Book, request.form["api_id"])
    if not book_entry:
        book_entry = Book.saveBook(request.form)
    if book_entry in g.user.books:
        flash("Book already in your reading list", "danger")
    else:
        try:
            g.user.books.append(book_entry)
            db.session.commit()
            flash("Book added to you reading list", "success")
        except:
            db.session.rollback()
            flash("Error adding book to your reading list", "danger")

    return redirect(url_for("user_page"))


@app.route("/user/<volume_id>", methods=["GET", "POST"])
@login_required
def user_book_page(volume_id):
    """View function to open book details and user information"""
    book_data = db.get_or_404(Book, volume_id)
    readLog = db.get_or_404(UserBook, (g.user.id, volume_id))
    statform = readStatisticsForm(obj=readLog)
    if statform.validate_on_submit():
        try:
            readLog.start_date = statform.start_date.data
            readLog.finish_date = statform.finish_date.data
            readLog.current_page = statform.current_page.data
            readLog.status = statform.status.data
            db.session.commit()
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>commited")
        except:
            db.session.rollback()
            print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< rolledback")
            flash("Error updating reading data, please try again")
    return render_template("user_book_page.html", book=book_data, form=statform)


"""
Book search engine
"""


@app.route("/search", methods=["GET"])
def search_books():
    """Route to execute book search queries. Replies with json file with search content"""
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
        books = []
        for item in data.get("items", []):
            if item["volumeInfo"]["language"] == "en":
                id = item.get("id")
                volume_info = item.get(
                    "volumeInfo", {}
                )  # volume is the google book term for an item (book, magazine or other content)
                data = {
                    "title": volume_info.get("title"),
                    "authors": volume_info.get("authors", []),
                    "publishedDate": volume_info.get("publishedDate"),
                    "description": volume_info.get("description"),
                    "thumbnail": volume_info.get("imageLinks", {}).get("thumbnail"),
                    "id": id,
                }
                books.append({"data": data})

        return jsonify(books)
    else:
        return jsonify(
            {"error": "Failed to fetch data please try again"}
        ), response.status_code


@app.route("/book/<volume_id>", methods=["GET"])
def get_book_details(volume_id):
    """Route to collect detailed information for a particular book volume"""
    params = {
        "key": api_key,
    }

    response = requests.get(url=f"{GOOGLE_BOOKS_API_URL}/{volume_id}", params=params)
    if response.status_code == 200:
        data = response.json()
        volume_info = data.get(
            "volumeInfo", {}
        )  # volume is the google book term for an item (book, magazine or other content)
        book_data = {
            "title": volume_info.get("title"),
            "authors": volume_info.get("authors", []),
            "categories": volume_info.get("categories", []),
            "publisher": volume_info.get("publisher"),
            "publishedDate": volume_info.get("publishedDate"),
            "description": volume_info.get("description"),
            "thumbnail": volume_info.get("imageLinks", {}).get("thumbnail"),
            "page_count": volume_info.get("pageCount"),
            "average_rating": volume_info.get("averageRating"),
            "id": volume_id,
        }
        return jsonify(book_data)
    else:
        return jsonify(
            {"error": "Failed to fetch data please try again"}
        ), response.status_code


"""
Book Comments engine
"""


@app.route("/comments/<volume_id>", methods=["GET"])
def get_all_book_comments(volume_id):
    """Route to read all available comments from a given book. Replies with json file with comments array"""
    comments = (
        db.session.query(Comment)
        .order_by(Comment.date)
        .filter_by(Comment.domain == 2)
        .all()
    )
    if not comments:
        return jsonify({"error": "Book not found in teh database"}), 400

    return jsonify(comments=[book.serialize() for book in comments])
