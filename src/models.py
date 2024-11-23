from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime, timezone

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
    clubs = db.relationship("Club", secondary="clubs_books", backref="books")

    # users -> users through users_books

    @classmethod
    def save_book(cls, data):
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
        db.Integer, default=0
    )  # Status should indicate 0-backlog, 1-reading, 2-postponed, 3-completed

    # user -> User connected to a readlog
    # book -> Book connected to the readlog

    def update_info(self, data):
        """Method to update user reading statistics"""
        self.start_date = data.get("start_date", self.start_date)
        self.finish_date = data.get("finish_date", self.finish_date)
        self.current_page = data.get("current_page", self.current_page)
        self.status = data.get("status", self.status)
        try:
            db.session.commit()
            return self
        except:
            db.session.rollback()
            return False

    def delete(self):
        """Method to remove book from user reading list"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False


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

    def update(self, data):
        """Method to update a book comment"""
        self.comment = data.get("comment", self.comment)
        self.rating = data.get("rating", self.rating)
        self.domain = data.get("domain", self.domain)
        self.date = date.today()
        try:
            db.session.commit()
            return self
        except:
            db.session.rollback()
            return False

    def serialize(self):
        """Method to convert the comment data into a dictionary"""
        return {
            "user_id": self.user_id,
            "book_id": self.book_id,
            "date": self.date,
            "comment": self.comment,
            "rating": self.rating,
            "username": self.user.first_name,
        }

    @classmethod
    def create_comment(cls, data):
        """Class function to create a new book comment"""
        new_comment = Comment(
            user_id=data["user_id"],
            book_id=data["book_id"],
            date=data["date"],
            comment=data["comment"],
            rating=data["rating"],
            domain=data["domain"],
        )
        try:
            db.session.add(new_comment)
            db.session.commit()
            return new_comment
        except:
            db.session.rollback()
            return False


class Club(db.Model):
    """Reading club database model
    Should contain basic information about the club"""

    __tablename__ = "clubs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Text)

    membership = db.relationship(
        "ClubMembers", backref="club", cascade="all, delete-orphan"
    )
    # members = User added to the club by clubs_users
    # books = book added to the club reading list through clubs_books

    def update(self, name, description):
        """Method to udpate the reading club information"""
        try:
            self.name = name
            self.description = description
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    def delete(self):
        """Method to delete the reading club"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    def add_book_to_list(self, book):
        """Method to add a book to the reading club list"""
        try:
            if book not in self.books:
                self.books.append(book)
                db.session.commit()
                return True
        except:
            db.session.rollback()
            return False

    @classmethod
    def create_club(cls, name, description, owner_id):
        """Class method to create new reading club in the database"""
        try:
            new_club = Club(name=name, description=description)
            db.session.add(new_club)
            db.session.flush()
            owner = ClubMembers.enrol_user(
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

    def delete(self):
        """Method to remove a book from the reading club"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False


class ClubMembers(db.Model):
    """Many to Many relationship between clubs and member users describing membership status.
    Should store details if the user has been invited, have accepted or rejected joining"""

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

    def accept_invite(self):
        """Method to accept an invitation to join a book club"""
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

    def reject_invite(self):
        """Method to reject an invitation to join a book club"""
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
        """Method to delete a member of the club (also valid for pending and rejected invites"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    @classmethod
    def enrol_user(cls, club_id, member_id, status):
        """Class method to invite a nem member to a club"""
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


class Message(db.Model):
    """Model for the messages int he forum for the reading clubs"""

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey("clubs.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    # user -> User who posted the message

    def serialize(self):
        """Method to convert a forum message to a dictionary"""
        return {
            "id": self.id,
            "message": self.message,
            "timestamp": self.timestamp.strftime("%d/%b/%y %I:%M %p"),
            "user_first_name": self.user.first_name,
            "user_last_name": self.user.last_name,
            "user_username": self.user.username,
        }

    def delete(self):
        """Method to delete a forum message"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            return False

    def update_message(self, message):
        """Method to update a forum message"""
        try:
            self.message = message
            db.session.commit()
            return self
        except:
            return False

    @classmethod
    def add_message(cls, club_id, user_id, message):
        """Class function to add a new message to the club forum"""
        new_message = Message(
            club_id=club_id,
            user_id=user_id,
            message=message,
            timestamp=datetime.now(timezone.utc),
        )
        try:
            db.session.add(new_message)
            db.session.commit()
            return new_message
        except:
            return False
