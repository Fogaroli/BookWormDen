from .database import db

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