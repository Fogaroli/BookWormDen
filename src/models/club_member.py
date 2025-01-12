from .database import db

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