
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Function to connect flask app to the database.
    """
    db.app = app
    db.init_app(app)

# Database model will go here.

class User(db.Model):
    """User account database model

    actions:
        Create database structure to store User Accounts.
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

    @classmethod
    def signup(cls, username, password, first_name, last_name, email):
        """Class method to create new users in the database
        """
        new_user = User(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
        db.session.add(new_user)
        db.session.commit
        return new_user
