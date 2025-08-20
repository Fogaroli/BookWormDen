from flask import Blueprint, render_template, redirect, url_for, flash, g, jsonify, request, current_app
import requests
from operator import and_
from .utils import login_required, club_access_required, login, logout
from forms import (
    UserAddForm,
    LoginForm,
    UserEditForm
)
from models import db, Book, Comment, Club, ClubMembers, ClubBook

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

book_route = Blueprint("book_route", __name__)


@book_route.route("/search", methods=["GET"])
def books_search_route():
    """Route to execute book search queries. Replies with json file with search content"""
    title_search = request.args.get("q", "")
    if not title_search:
        return jsonify({"error": "Please enter a book title to search"}), 400
    api_key = current_app.config["GOOGLE_API_KEY"]
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


@book_route.route("/book/<volume_id>", methods=["GET"])
def book_details_route(volume_id):
    """Route to collect detailed information for a particular book volume"""
    api_key = current_app.config["GOOGLE_API_KEY"]
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


@book_route.route("/book/<volume_id>/clubs", methods=["GET"])
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


@book_route.route("/book/<volume_id>/add", methods=["POST"])
@login_required
def add_book_club_reading_list(volume_id):
    """Route to add a book to the reading club book list"""
    json_data = request.get_json()
    club_name = json_data.get("club_name")
    book = db.get_or_404(Book, volume_id)
    club = db.session.query(Club).filter(Club.name == club_name).first()
    added = club.add_book_to_list(book)
    if added:
        data = {"book": book.title, "club": club.name}
        return jsonify(added=data), 200
    else:
        return jsonify(json_data), 400


@book_route.route("/book/<volume_id>/delete", methods=["POST"])
@login_required
def remove_book_club_reading_list(volume_id):
    """Route to remove a book from the reading club book list"""
    json_data = request.get_json()
    club_id = json_data.get("club_id")
    club = db.get_or_404(Club, club_id)
    book = db.get_or_404(Book, volume_id)
    owner = (
        db.session.query(ClubMembers)
        .filter(and_(ClubMembers.club_id == club_id, ClubMembers.status == 1))
        .first()
    )
    if owner.member_id == g.user.id:
        book_list = db.get_or_404(ClubBook, (club_id, volume_id))
        deleted = book_list.delete()
        if deleted:
            data = {"book": book.title, "club": club.name}
            return jsonify(deleted=data), 200
        else:
            return jsonify(json_data), 400
    else:
        return jsonify(json_data), 500


"""
Book Comments Route
"""


@book_route.route("/comments/<volume_id>", methods=["GET"])
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
        return jsonify({"error": "No comments found in the database"}), 400

    return jsonify(comments=[book_comment.serialize() for book_comment in comments])