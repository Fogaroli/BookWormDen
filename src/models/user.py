from .database import db

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()


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

    books = db.relationship("Book", secondary="users_books", backref="users")
    readlog = db.relationship("UserBook", backref="user")
    comments = db.relationship("Comment", backref="user")
    membership = db.relationship("ClubMembers", backref="user")
    messages = db.relationship("Message", backref="user")

    def validate_user(self, password):
        """Method to validate entered password, comparing to stored hashed password"""
        return self if bcrypt.check_password_hash(self.password, password) else False

    def update_info(self, data):
        """Method to update user data"""
        self.first_name = data.get("first_name", self.first_name)
        self.last_name = data.get("last_name", self.last_name)
        self.email = data.get("email", self.email)
        self.image_url = data.get("image_url", self.image_url)
        self.bio = data.get("bio", self.bio)
        self.location = data.get("location", self.location)
        try:
            db.session.commit()
            return self
        except:
            db.session.rollback()
            return False

    def update_password(self, new_password):
        """Method to update password"""
        try:
            hashed_password = bcrypt.generate_password_hash(new_password).decode("utf8")
            self.password = hashed_password
            db.session.commit()
            return self
        except:
            db.session.rollback()
            return False

    def add_to_reading_list(self, book):
        """Method to add a book to the user reading list"""
        try:
            self.books.append(book)
            db.session.commit()
            return self.books
        except:
            return False

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