"""
File used to enter basic data into the database

"""

import bcrypt
from app import app
from models import db, User, Book, UserBook, Comment
from flask_bcrypt import Bcrypt
from datetime import datetime, date, timedelta

# Clear database
with app.app_context():
    db.drop_all()
    db.create_all()

bcrypt = Bcrypt()

if __name__ == "__main__":
    app.app_context().push()

user1 = User(
    username="fabricio",
    password=bcrypt.generate_password_hash("fabricio").decode("utf8"),
    email="fogaroli@gmail.com",
    first_name="Fabricio",
    last_name="Ribeiro",
    bio="Just trying to get there",
    location="Porto, Portugal",
)

db.session.add_all([user1])
db.session.commit()
