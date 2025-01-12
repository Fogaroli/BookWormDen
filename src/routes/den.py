from flask import Blueprint, render_template, redirect, url_for, flash, g, jsonify, request
from datetime import date
from .utils import login_required, club_access_required, login, logout
from forms import (
    ReadStatisticsForm,
    NewCommentForm
)
from models import db, Book, UserBook, Comment

den_route = Blueprint("den_route", __name__)


@den_route.route("/", methods=["GET"])
@login_required
def user_den_view():
    """View function to open user home den"""
    reading_log = g.user.readlog
    return render_template("den_page.html", list=reading_log)


@den_route.route("/add-book", methods=["POST"])
@login_required
def add_book_to_user():
    """View function to add a volume to the user reading list.
    If the book does not exist in the local database, this function will add it (to the database) before adding to the user reading list.
    """
    book_entry = db.session.get(Book, request.form["api_id"])
    if not book_entry:
        book_entry = Book.save_book(request.form)
    if book_entry in g.user.books:
        flash("Book already in your reading list", "danger")
    else:
        book_added = g.user.add_to_reading_list(book_entry)
        if book_added:
            flash("Book added to your reading list", "success")
        else:
            flash("Error adding book to your reading list", "danger")

    return redirect(url_for("den_route.user_den_view"))


@den_route.route("/<volume_id>/delete", methods=["POST"])
@login_required
def remove_book_from_user(volume_id):
    """View function to remove a volume from the user reading list.
    The book should remain in the database.
    """
    readlog = db.get_or_404(UserBook, (g.user.id, volume_id))
    deleted = readlog.delete()
    if deleted:
        flash("Book removed from your reading list", "success")
    else:
        flash("Error removing the book, please try again", "danger")
    return redirect(url_for("den_route.user_den_view"))


@den_route.route("/<volume_id>", methods=["GET", "POST"])
@login_required
def book_view(volume_id):
    """View function to open book details and user information"""
    readlog = db.session.query(UserBook).filter_by(user_id=g.user.id, book_id=volume_id).first()
    if not readlog:
        flash("Book not added to your den, add it first", "danger")
        return redirect(request.referrer or url_for("den_route.user_den_view"))
    stat_form = ReadStatisticsForm(obj=readlog)
    user_comment = db.session.get(Comment, (g.user.id, volume_id))
    comment_form = NewCommentForm(obj=user_comment)

    if (
        request.method == "POST"
        and stat_form.validate_on_submit()
        and request.form.get("submit") == "statform"
    ):
        updated = readlog.update_info(stat_form.data)
        if updated:
            flash("Information updated", "success")
        else:
            flash("Error updating information, please try again", "success")
        return redirect(url_for("den_route.book_view", volume_id=volume_id))
    if (
        request.method == "POST"
        and comment_form.validate_on_submit()
        and request.form.get("submit") == "commentform"
    ):
        if user_comment:
            updated = user_comment.update(comment_form.data)
            if updated:
                flash("Comment updated successfully", "success")
            else:
                flash("Error updating your comment", "danger")
            return redirect(url_for("den_route.book_view", volume_id=volume_id))
        else:
            new_comment_data = {
                **comment_form.data,
                "user_id": g.user.id,
                "book_id": volume_id,
                "date": date.today(),
            }
            new_comment = Comment.create_comment(new_comment_data)
            if new_comment:
                flash("Comment added successfully", "success")
            else:
                flash("Error adding your comment", "danger")
            return redirect(url_for("den_route.book_view", volume_id=volume_id))

    book_data = db.get_or_404(Book, volume_id)
    return render_template(
        "book.html",
        book=book_data,
        statform=stat_form,
        commentform=comment_form,
    )