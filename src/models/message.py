from .database import db

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