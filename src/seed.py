"""
File used to enter basic data into the database

"""

from app import app
from models import db, User

# Clear database
with app.app_context():
    db.drop_all()
    db.create_all()

user1 = User(
    username="fabricio",
    password="fabricio",
    email="fabricio@me.com",
    first_name="Fabricio",
    last_name="Ribeiro",
)

user2 = User(
    username="BigWorm",
    password="bigworm",
    email="bfwamr@test.com",
    first_name="Very Big",
    last_name="Worm",
)


with app.app_context():
    db.session.add_all([user1, user2])
    db.session.commit()
