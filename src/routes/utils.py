"""
BoomWorm Den Supporting functions
"""

from functools import wraps
from flask import session, flash, redirect, url_for, g, request

def login_required(f):
    """Decorator function to control protected views"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "CURRENT_USER" not in session:
            flash("Please login first", "danger")
            return redirect(url_for("user_route.login_view", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


def club_access_required(f):
    """
    Decorator to check if the current user has access to the specified club.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        club_id = int(kwargs.get("club_id"))
        member_club_ids = [
            membership.club.id
            for membership in g.user.membership
            if membership.status in [1, 2]
        ]
        if club_id not in member_club_ids:
            flash("You don't have access to this club", "danger")
            return redirect(url_for("club_route.clubs_view"))

        return f(*args, **kwargs)

    return decorated_function


def login(user):
    """Function to process login, store user information on flask session"""
    session["CURRENT_USER"] = user.id


def logout():
    """Function to process logout, remove user information from flask session"""
    session.pop("CURRENT_USER")