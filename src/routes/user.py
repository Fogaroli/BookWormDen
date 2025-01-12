from flask import Blueprint, render_template, redirect, url_for, flash, g, jsonify, session, request
from sqlalchemy import func
from .utils import login_required, club_access_required, login, logout
from forms import (
    UserEditForm,
)
from models import db, User


user_route = Blueprint("user_route", __name__)

@user_route.route("/", methods=["GET", "POST"])
@login_required
def profile_view():
    """View function to open user info and edit page"""
    edit_form = UserEditForm(obj=g.user)
    if request.method == "POST" and edit_form.validate_on_submit():
        button = request.form.get("button")
        if button == "save":
            updated = g.user.update_info(edit_form.data)
            if updated:
                flash("User profile updated", "success")
            else:
                flash("Error updating profile, please try again", "danger")
            return redirect(url_for("user_route.profile_view"))
        if button == "change_password":
            if g.user.validate_user(edit_form.password.data):
                password_updated = g.user.update_password(edit_form.new_password.data)
                if password_updated:
                    flash("Password updated", "success")
                else:
                    flash(
                        "Error changing password, please use old password and try again",
                        "danger",
                    )
                return redirect(url_for("user_route.profile_view"))
            else:
                flash(
                    "Error changing password, please use old password and try again",
                    "danger",
                )
    return render_template("profile_page.html", user=g.user, form=edit_form)


@user_route.route("/search", methods=["GET"])
@login_required
def user_search_route():
    """Route to search for users based on a provided argument"""
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