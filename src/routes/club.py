from flask import Blueprint, render_template, redirect, url_for, flash, g, jsonify, request
from .utils import login_required, club_access_required, login, logout
from forms import NewClubForm
from models import db, Club, ClubMembers, User


club_route = Blueprint("club_route", __name__)

@club_route.route("/", methods=["GET", "POST"])
@login_required
def clubs_view():
    """View function to open user book clubs home"""

    club_form = NewClubForm()
    if request.method == "POST" and club_form.validate_on_submit():
        new_club = Club.create_club(
            name=club_form.name.data,
            description=club_form.description.data,
            owner_id=g.user.id,
        )
        if new_club:
            flash("Reading club added to the database", "success")
        else:
            flash("Error adding the reading club, please try again", "danger")
        return redirect(url_for("club_route.clubs_view"))
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


@club_route.route("/<club_id>", methods=["GET"])
@login_required
@club_access_required
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

    return render_template("club.html", club=club, memberships=memberships, owner=owner)


@club_route.route("/<club_id>/edit", methods=["GET", "POST"])
@login_required
def edit_club_view(club_id):
    """View function to edit user book information"""
    club = db.get_or_404(Club, club_id)
    club_form = NewClubForm(obj=club, current_name=club.name)
    if request.method == "POST" and club_form.validate_on_submit():
        updated_club = club.update(
            name=club_form.name.data,
            description=club_form.description.data,
        )
        if updated_club:
            flash("Reading club updated", "success")
        else:
            flash("Error updating the reading club, please try again", "danger")
        return redirect(url_for("club_route.edit_club_view", club_id=club_id))
    return render_template("edit_club_page.html", form=club_form, club_id=club_id)


@club_route.route("/delete", methods=["POST"])
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
    return redirect(url_for("club_route.clubs_view"))


@club_route.route("/<club_id>/add", methods=["POST"])
@login_required
def add_user_route(club_id):
    """Route to add a member to a reading club"""
    json_data = request.get_json()
    user = db.session.query(User).filter(User.username == json_data["username"]).first()
    if user:
        new_membership = ClubMembers.enrol_user(
            club_id=club_id, member_id=user.id, status=3
        )
    else:
        new_membership = False
    if new_membership:
        data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        return jsonify(added_member=data), 200
    else:
        return jsonify(json_data), 400


@club_route.route("/<club_id>/delete", methods=["POST"])
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


@club_route.route("/<club_id>/invite", methods=["POST"])
@login_required
def process_invite_route(club_id):
    """Route to process a reading club invitation, either accept or reject"""
    response = request.form.get("invite")
    membership = db.get_or_404(ClubMembers, (club_id, g.user.id))
    if response == "accept":
        accept = membership.accept_invite()
        if accept:
            flash(f"You joined {membership.club.name}", "success")
        else:
            flash("Error processing your response, please try again", "danger")

    if response == "reject":
        reject = membership.reject_invite()
        if reject:
            flash(f"You reject to join {membership.club.name}", "warning")
        else:
            flash("Error processing your response, please try again", "danger")
    return redirect(url_for("club_route.clubs_view"))

