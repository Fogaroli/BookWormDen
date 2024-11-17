"""
================================================================
Title: Book Worm Den
Author: Fabricio Ribeiro
Date: September 17, 2024

================================================================
"""

from operator import and_, methodcaller
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
from models import db, connect_db, User, Book, UserBook, Comment, Club, ClubMembers
from forms import (
    UserAddForm,
    LoginForm,
    ReadStatisticsForm,
    NewCommentForm,
    NewClubForm,
)
import requests
from datetime import date
from sqlalchemy import func

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
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
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


@app.route("/", methods=["GET"])
def homepage():
    """View Function for the portal homepage."""
    return render_template("homepage.html")


"""
User views
"""


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
            return redirect(url_for("user_den_view"))
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
def user_view():
    """View function to open user homepage"""
    return render_template("user_page.html", user=g.user)


@app.route("/user/search", methods=["GET"])
@login_required
def user_search_route():
    string = request.args.get("q", "")
    if string:
        users = (
            db.session.query(User)
            .filter(
                func.concat(User.first_name, " ", User.last_name).ilike(f"%{string}%")
            )
            .all()
        )
        suggestions = [
            f"{user.first_name} {user.last_name} - {user.username}" for user in users
        ]
    else:
        suggestions = []
    return jsonify(suggestions)


"""
User den routes
"""


@app.route("/den", methods=["GET"])
@login_required
def user_den_view():
    """View function to open user home den"""
    reading_log = g.user.readlog
    return render_template("den_page.html", list=reading_log)


@app.route("/den/add-book", methods=["POST"])
@login_required
def add_book_to_user():
    """View function to add a volume to the user reading list.
    If the book does not exist in the local database, this function will add it (to the database) before adding to the user reading list.
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

    return redirect(url_for("user_den_view"))


@app.route("/den/<volume_id>", methods=["GET", "POST"])
@login_required
def user_book_view(volume_id):
    """View function to open book details and user information"""
    read_log = db.get_or_404(UserBook, (g.user.id, volume_id))
    stat_form = ReadStatisticsForm(obj=read_log)
    user_comment = db.session.get(Comment, (g.user.id, volume_id))
    comment_form = NewCommentForm(obj=user_comment)

    if stat_form.validate_on_submit() and request.form.get("submit") == "statform":
        try:
            read_log.start_date = stat_form.start_date.data
            read_log.finish_date = stat_form.finish_date.data
            read_log.current_page = stat_form.current_page.data
            read_log.status = stat_form.status.data
            db.session.commit()
        except:
            db.session.rollback()
            flash("Error updating reading data, please try again", "danger")

    if (
        comment_form.validate_on_submit()
        and request.form.get("submit") == "commentform"
    ):
        if user_comment:
            try:
                user_comment.comment = comment_form.comment.data
                user_comment.rating = comment_form.rating.data
                user_comment.domain = comment_form.domain.data
                user_comment.date = date.today()
                db.session.commit()
                flash("Comment updated successfully", "success")
            except:
                db.session.rollback()
                flash("Error updating your comment", "danger")
        else:
            try:
                new_comment = Comment(
                    user_id=g.user.id,
                    book_id=volume_id,
                    date=date.today(),
                    comment=comment_form.comment.data,
                    rating=comment_form.rating.data,
                    domain=comment_form.domain.data,
                )
                db.session.add(new_comment)
                db.session.commit()
                flash("Comment added successfully", "success")
            except:
                db.session.rollback()
                flash("Error adding your comment", "danger")
    book_data = db.get_or_404(Book, volume_id)
    return render_template(
        "user_book.html",
        book=book_data,
        statform=stat_form,
        commentform=comment_form,
    )


"""
Book search routes
"""


@app.route("/search", methods=["GET"])
def books_search_route():
    """Route to execute book search queries. Replies with json file with search content"""
    title_search = request.args.get("q", "")
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
def book_details_route(volume_id):
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
            "title": volume_info.get("title", ""),
            "authors": volume_info.get("authors", []),
            "categories": volume_info.get("categories", []),
            "publisher": volume_info.get("publisher", ""),
            "publishedDate": volume_info.get("publishedDate"),
            "description": volume_info.get("description", ""),
            "thumbnail": volume_info.get("imageLinks", {}).get("thumbnail"),
            "page_count": volume_info.get("pageCount", 0),
            "average_rating": volume_info.get("averageRating", 0),
            "id": volume_id,
        }
        return jsonify(book_data)
    else:
        return jsonify(
            {"error": "Failed to fetch data please try again"}
        ), response.status_code


@app.route("/book/<volume_id>/clubs", methods=["GET"])
@login_required
def book_club_reading_list(volume_id):
    """Route to collect the reading clubs from a the connected user and if the given book is already in the reading list"""
    book = db.get_or_404(Book, volume_id)
    user_member_clubs = [
        membership.club
        for membership in g.user.membership
        if membership.status in [1, 2]
    ]
    included_clubs = [club.name for club in user_member_clubs if club in book.clubs]
    club_choices = [club.name for club in user_member_clubs if club not in book.clubs]

    return jsonify(included=included_clubs, choices=club_choices)


@app.route("/book/<volume_id>/add", methods=["POST"])
@login_required
def add_book_club_reading_list(volume_id):
    """Route to add a book to the reading club book list"""
    json_data = request.get_json()
    club_name = json_data.get("club_name")
    book = db.get_or_404(Book, volume_id)
    club = db.session.query(Club).filter(Club.name == club_name).first()
    added = club.addBookToList(book)
    if added:
        return jsonify(book=book.title, club=club.name), 200
    else:
        return jsonify(json_data), 400


"""
Book Comments Route
"""


@app.route("/comments/<volume_id>", methods=["GET"])
@login_required
def book_comments_route(volume_id):
    """Route to read all available comments from a given book. Replies with json file with comments array"""
    comments = (
        db.session.query(Comment)
        .order_by(Comment.date)
        .filter(and_(Comment.book_id == volume_id, Comment.domain == 2))
        .all()
    )
    if not comments:
        return jsonify({"error": "Book not found in the database"}), 400

    return jsonify(comments=[book_comment.serialize() for book_comment in comments])


"""
Book clubs Views
"""


@app.route("/clubs", methods=["GET", "POST"])
@login_required
def book_clubs_view():
    """View function to open user book clubs home"""

    club_form = NewClubForm()
    if club_form.validate_on_submit():
        new_club = Club.createClub(
            name=club_form.name.data,
            description=club_form.description.data,
            owner_id=g.user.id,
        )
        if new_club:
            flash("Reading club added to the database", "success")
        else:
            flash("Error adding the reading club, please try again", "danger")
    clubs_member = [
        membership.club for membership in g.user.membership if membership.status == 2
    ]
    clubs_owner = [
        membership.club for membership in g.user.membership if membership.status == 1
    ]
    clubs_invited = [
        membership.club for membership in g.user.membership if membership.status == 3
    ]
    return render_template(
        "clubs_page.html",
        form=club_form,
        owned=clubs_owner,
        member=clubs_member,
        invited=clubs_invited,
    )


@app.route("/clubs/<club_id>", methods=["GET"])
@login_required
def club_view(club_id):
    """View function to open book club information"""
    club = db.get_or_404(Club, club_id)
    owner = next(
        (member.user for member in club.membership if member.status == 1), None
    )
    memberships = (
        db.session.query(ClubMembers)
        .filter(ClubMembers.club_id == club_id)
        .order_by(ClubMembers.status)
    )

    return render_template(
        "user_club.html", club=club, memberships=memberships, owner=owner
    )


@app.route("/clubs/<club_id>/edit", methods=["GET", "POST"])
@login_required
def edit_club_view(club_id):
    """View function to edit user book information"""
    club = db.get_or_404(Club, club_id)
    club_form = NewClubForm(obj=club)
    if club_form.validate_on_submit():
        updated_club = club.updateClub(
            name=club_form.name.data,
            description=club_form.description.data,
        )
        if updated_club:
            flash("Reading club updated", "success")
        else:
            flash("Error updating the reading club, please try again", "danger")
    return render_template("club_edit_page.html", form=club_form, club_id=club_id)


@app.route("/clubs/delete", methods=["POST"])
@login_required
def delete_club_route():
    """View function to edit user book information"""
    club_id = request.form["club_id"]
    club = db.get_or_404(Club, club_id)
    deleted = club.delete()
    if deleted:
        flash("Club deleted", "success")
    else:
        flash("Error deleting the reading club, please try again", "danger")
    return redirect(url_for("book_clubs_view"))


@app.route("/clubs/<club_id>/add", methods=["POST"])
@login_required
def add_user_route(club_id):
    """Route to add a member to a reading club"""
    json_data = request.get_json()
    user = db.session.query(User).filter(User.username == json_data["username"]).first()
    new_membership = ClubMembers.enrolUser(club_id=club_id, member_id=user.id, status=3)
    if new_membership:
        data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        return jsonify(added_member=data), 200
    else:
        return jsonify(json_data), 400


@app.route("/clubs/<club_id>/delete", methods=["POST"])
@login_required
def delete_user_route(club_id):
    """Route to add a member to a reading club"""
    json_data = request.get_json()
    user = db.session.query(User).filter(User.username == json_data["username"]).first()
    membership = db.get_or_404(ClubMembers, (club_id, user.id))
    delete = membership.delete()
    if delete:
        data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        return jsonify(removed_member=data), 200
    else:
        return jsonify(json_data), 400


@app.route("/clubs/<club_id>/invite", methods=["POST"])
@login_required
def process_invite_route(club_id):
    response = request.form.get("invite")
    membership = db.get_or_404(ClubMembers, (club_id, g.user.id))
    if response == "accept":
        accept = membership.acceptInvite()
        if accept:
            flash(f"You joined {membership.club.name}", "success")
        else:
            flash("Error processing your response, please try again", "danger")

    if response == "reject":
        reject = membership.rejectInvite()
        if reject:
            flash(f"You reject to join {membership.club.name}", "warning")
        else:
            flash("Error processing your response, please try again", "danger")
    return redirect(url_for("book_clubs_view"))
