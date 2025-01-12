from flask import Blueprint, render_template, redirect, url_for, flash, g, jsonify, request
from .utils import login_required, club_access_required, login, logout
from models import db, Message


forum_route = Blueprint("forum_route", __name__)

@forum_route.route("/<club_id>/messages", methods=["GET"])
@login_required
@club_access_required
def club_messages_route(club_id):
    """Route to read all available messages for a given club"""
    start = request.args.get("start", 0)
    quantity = request.args.get("quantity", 20)
    messages = (
        db.session.query(Message)
        .filter(Message.club_id == club_id)
        .order_by(Message.timestamp.desc())
        .offset(start)
        .limit(quantity)
    )
    data = [message.serialize() for message in messages]
    return jsonify(messages=data), 200


@forum_route.route("/<club_id>/messages", methods=["POST"])
@login_required
@club_access_required
def add_club_messages_route(club_id):
    """Route to add a new message to the club forum"""
    json_data = request.get_json()
    new_message = Message.add_message(
        club_id=club_id, user_id=g.user.id, message=json_data["message"]
    )
    if new_message:
        return jsonify(message=new_message.serialize()), 200
    return jsonify(json_data), 400


@forum_route.route("/<club_id>/messages/<message_id>", methods=["PATCH"])
@login_required
@club_access_required
def update_club_messages_route(club_id, message_id):
    """Route to update message content from am existing message"""
    json_data = request.get_json()
    message = db.get_or_404(Message, message_id)
    if message.user_id != g.user.id or message.club_id != int(club_id):
        return jsonify(json_data), 403
    modified = message.update_message(json_data.get("message", message.message))
    if modified:
        return jsonify(message=modified.serialize()), 200
    return jsonify(json_data), 400


@forum_route.route("/<club_id>/messages/<message_id>", methods=["DELETE"])
@login_required
@club_access_required
def delete_club_messages_route(club_id, message_id):
    """Route to delete an existing message"""
    json_data = request.get_json()
    message = db.get_or_404(Message, message_id)
    if message.user_id != g.user.id or message.club_id != int(club_id):
        return jsonify(json_data), 403
    deleted = message.delete()
    if deleted:
        return jsonify(message="deleted"), 200
    return jsonify(json_data), 400