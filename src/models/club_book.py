
from .database import db

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