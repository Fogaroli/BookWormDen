from .database import db


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