
from .database import db
from .club_member import ClubMembers

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
            return False
        except Exception:
            db.session.rollback()
            return False