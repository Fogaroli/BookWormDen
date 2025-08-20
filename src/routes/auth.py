from flask import Blueprint, render_template, redirect, url_for, flash, g, jsonify, session, request
from sqlalchemy import func
from .utils import login_required, club_access_required, login, logout
from forms import (
    UserAddForm,
    LoginForm,
)
from models import db, User


auth_route = Blueprint("auth_route", __name__)

@auth_route.route("/register", methods=["GET", "POST"])
def registration_view():
    """View function for new user registration"""

    registration_form = UserAddForm()
    if registration_form.validate_on_submit():
        new_user = User.signup(registration_form.data)
        if new_user:
            flash(f"Welcome {new_user.first_name} to the BookwormDen", "success")
            login(new_user)
            return redirect(url_for("den_route.user_den_view"))
        else:
            flash("Error creating new user, please try again", "danger")

    return render_template("user_signup.html", form=registration_form)


@auth_route.route("/login", methods=["GET", "POST"])
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
            return redirect(url_for("den_route.user_den_view"))
        else:
            flash("User and/or password invalid, please try again", "danger")
    return render_template("user_login.html", form=login_form)


@auth_route.route("/logout", methods=["POST"])
def logout_view():
    """View function for user logout"""
    if g.user:
        logout()
    return redirect(url_for("homepage"))