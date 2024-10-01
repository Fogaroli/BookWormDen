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
    email="fogaroli@gmail.com",
    first_name="Fabricio",
    last_name="Ribeiro",
)

user2 = User(
    username="mainworm",
    password=bcrypt.generate_password_hash("bigworm").decode("utf8"),
    email="bfworm@test.com",
    first_name="Main",
    last_name="Worm",
)


with app.app_context():
    db.session.add_all([user1, user2])
    db.session.commit()
