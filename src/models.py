from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Function to connect flask app to the database."""
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
    image_url = db.Column(db.Text)
    bio = db.Column(db.Text)
    location = db.Column(db.String(30))

    def validate_user(self, password):
        """Function to validate entered password, comparing to stored hashed password"""
        return self if bcrypt.check_password_hash(self.password, password) else False

    @classmethod
    def signup(cls, data):
        """Class method to create new users in the database"""
        try:
            hashed_password = bcrypt.generate_password_hash(data["password"]).decode(
                "utf8"
            )
            new_user = User(
                username=data["username"],
                password=hashed_password,
                email=data["email"],
                first_name=data["first_name"],
                last_name=data["last_name"],
            )
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except:
            db.session.rollback()
            return False