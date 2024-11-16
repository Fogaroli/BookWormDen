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

    books = db.relationship("Book", secondary="users_books", backref="users")
    readlog = db.relationship("UserBook", backref="user")
    comments = db.relationship("Comment", backref="user")
    membership = db.relationship("ClubMembers", backref="user")

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


class Book(db.Model):
    """Book records database model
    Should contain basic information about books that are indexed in the portal.

    """

    __tablename__ = "books"

    api_id = db.Column(db.String(30), primary_key=True)
    title = db.Column(db.Text, nullable=False)
    cover = db.Column(db.Text, nullable=False)
    authors = db.Column(db.Text)
    categories = db.Column(db.Text)
    description = db.Column(db.Text)
    page_count = db.Column(db.Integer)

    userlog = db.relationship("UserBook", backref="book")
    comments = db.relationship("Comment", backref="book")
    clubs = db.relationship("Club", secondary="clubs_books", backref="books")

    # users -> users through users_books

    @classmethod
    def saveBook(cls, data):
        """Class method to save a new book to the database"""
        try:
            new_book = Book(**data)
            db.session.add(new_book)
            db.session.commit()
            return new_book
        except:
            db.session.rollback()
            return False


class UserBook(db.Model):
    """Model for many to many relationship between users and books"""

    __tablename__ = "users_books"

    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), primary_key=True, nullable=False
    )
    book_id = db.Column(
        db.String, db.ForeignKey("books.api_id"), primary_key=True, nullable=False
    )
    start_date = db.Column(db.Date)
    finish_date = db.Column(db.Date)
    current_page = db.Column(db.Integer)
    status = db.Column(
        db.Integer
    )  # Status should indicate 0-backlog, 1-reading, 2-postponed, 3-completed

    # user -> User connected to a readlog
    # book -> Book connected to the readlog


class Comment(db.Model):
    """Model for the book comments added by users to each book"""

    __tablename__ = "comments"

    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), primary_key=True, nullable=False
    )
    book_id = db.Column(
        db.String, db.ForeignKey("books.api_id"), primary_key=True, nullable=False
    )
    date = db.Column(db.Date)
    comment = db.Column(db.Text)
    rating = db.Column(db.Numeric)
    domain = db.Column(
        db.Integer
    )  # Should indicate the audience of the comment (1=Internal, 2 = Public)

    # user -> User owner of the comment
    # book -> Book connected to the comment

    def serialize(self):
        return {
            "user_id": self.user_id,
            "book_id": self.book_id,
            "date": self.date,
            "comment": self.comment,
            "rating": self.rating,
            "username": self.user.first_name,
        }


class Club(db.Model):
    """Reading club database model
    Should contain basic information about the club"""

    __tablename__ = "clubs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Text)

    members = db.relationship(
        "ClubMembers", backref="club", cascade="all, delete-orphan"
    )

    # books = book added to the club reading list through clubs_books

    def updateClub(self, name, description):
        try:
            self.name = name
            self.description = description
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    @classmethod
    def createClub(cls, name, description, owner_id):
        """Class method to create new reading club in the database"""
        try:
            new_club = Club(name=name, description=description)
            db.session.add(new_club)
            db.session.flush()
            owner = ClubMembers.enrolUser(
                club_id=new_club.id, member_id=owner_id, status=1
            )
            if owner:
                db.session.commit()
                return new_club
            else:
                raise Exception()
        except Exception:
            db.session.rollback()
            return False


class ClubBook(db.Model):
    """Model for many to many relationship between reading clubs and books"""

    __tablename__ = "clubs_books"

    club_id = db.Column(
        db.Integer, db.ForeignKey("clubs.id"), primary_key=True, nullable=False
    )
    book_id = db.Column(
        db.String, db.ForeignKey("books.api_id"), primary_key=True, nullable=False
    )


class ClubMembers(db.Model):
    """Many to Many relationship between clubs and member users.
    Should also store details if the user has been invited, have accepted or rejected joining"""

    __tablename__ = "clubs_users"

    club_id = db.Column(db.Integer, db.ForeignKey("clubs.id"), primary_key=True)
    member_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), primary_key=True, nullable=False
    )
    status = db.Column(
        db.Integer
    )  # Should indicate the membership status (1= owner, 2 = member, 3 = invited, 4 = rejected)

    # user -> User connected to membership
    # club -> Club connected to membership

    def acceptInvite(self):
        try:
            if self.status != 1:
                self.status = 2
                db.session.commit()
                return True
            else:
                db.session.rollback()
                raise Exception()
        except:
            return False

    def rejectInvite(self):
        try:
            if self.status != 1:
                self.status = 4
                db.session.commit()
                return True
            else:
                db.session.rollback()
                raise Exception()
        except:
            return False

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    @classmethod
    def enrolUser(cls, club_id, member_id, status):
        """Class method to register a nem member to a club"""
        try:
            new_membership = ClubMembers(
                club_id=club_id, member_id=member_id, status=status
            )
            db.session.add(new_membership)
            db.session.commit()
            return new_membership
        except:
            db.session.rollback()
            return False
