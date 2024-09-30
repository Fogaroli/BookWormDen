"""
File used to enter basic data into the database

"""

import bcrypt
from app import app
from models import db, User
from flask_bcrypt import Bcrypt

# Clear database
with app.app_context():
    db.drop_all()
    db.create_all()

bcrypt = Bcrypt()

user1 = User(
    username="fabricio",
    password=bcrypt.generate_password_hash("fabricio").decode("utf8"),
    email="fabricio@me.com",
    first_name="Fabricio",
    last_name="Ribeiro",
)

user2 = User(
    username="BigWorm",
    password=bcrypt.generate_password_hash("bigworm").decode("utf8"),
    email="bfwamr@test.com",
    first_name="Very Big",
    last_name="Worm",
)


with app.app_context():
    db.session.add_all([user1, user2])
    db.session.commit()
