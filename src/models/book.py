from .database import db

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