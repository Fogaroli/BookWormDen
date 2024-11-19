from flask_wtf import FlaskForm
from sqlalchemy import URL
from models import db, Club, User
from wtforms import (
    StringField,
    PasswordField,
    DateField,
    SelectField,
    IntegerField,
    TextAreaField,
    DecimalField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    Optional,
    ValidationError,
    URL,
    Regexp,
)


class UserAddForm(FlaskForm):
    """Form for user registration."""

    first_name = StringField("First name", validators=[DataRequired(), Length(max=50)])
    last_name = StringField("Last name", validators=[DataRequired(), Length(max=50)])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Regexp(
                regex="^(?=.{6,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).*$",
                message="Password must have 6 characters minimum, UPPERCASE, lowercase and numeric character",
            ),
        ],
    )

    def validate_username(form, field):
        if " " in field.data or "-" in field.data:
            raise ValidationError("Username must not contain spaces or dashes.")

    def validate_email(form, field):
        database_list = db.session.query(User.email).all()
        if field.data in database_list:
            raise ValidationError("This E-mail is already in the database")


class UserEditForm(FlaskForm):
    """Form for user information editing."""

    first_name = StringField("First name", validators=[DataRequired(), Length(max=50)])
    last_name = StringField("Last name", validators=[DataRequired(), Length(max=50)])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    image_url = StringField("Portrait (Avatar) URL", validators=[Optional(), URL()])
    bio = TextAreaField("A bit about yorself", validators=[Optional()])
    location = StringField("City, Country", validators=[Optional])
    password = PasswordField("Password", validators=[Length(min=6)])
    new_password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Regexp(
                regex="^(?=.{6,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).*$",
                message="Password must have 6 characters minimum, UPPERCASE, lowercase and numeric character",
            ),
        ],
    )

    def validate_email(form, field):
        database_list = db.session.query(User.email).all()
        if field.data in database_list:
            raise ValidationError("This E-mail is already in the database")


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])


class ReadStatisticsForm(FlaskForm):
    """Form to record the reading statistics for a specified book"""

    start_date = DateField(
        "Date I started reading the book", format="%Y-%m-%d", validators=[Optional()]
    )
    finish_date = DateField(
        "Date I finished dreading the book", format="%Y-%m-%d", validators=[Optional()]
    )
    current_page = IntegerField("Page I last read", validators=[Optional()])
    status = SelectField(
        "Current Status",
        choices=[
            (0, "In the list"),
            (1, "Reading"),
            (2, "Taking a pause"),
            (3, "Done"),
        ],
        coerce=int,
        validators=[Optional()],
    )


class NewCommentForm(FlaskForm):
    """Form used to register a new book comment"""

    comment = TextAreaField(
        "Enter your impressions about the book", validators=[Optional()]
    )
    rating = DecimalField(
        "Enter a rating from 0 to 5",
        places=1,
        validators=[
            Optional(),
            NumberRange(min=0, max=5, message="Rating must be between 0 and 5"),
        ],
    )
    domain = SelectField(
        "Select audience for your comment",
        choices=[
            (1, "Private (my eyes only)"),
            (2, "Public (visible to all Den's members)"),
        ],
    )


class NewClubForm(FlaskForm):
    """Form to create a mew reading club"""

    name = StringField("Reading Club Name", validators=[DataRequired(), Length(max=50)])
    description = TextAreaField("Club Description", validators=[Optional()])

    def validate_name(form, field):
        clubs = db.session.query(Club).all()
        club_names = [club.name for club in clubs]
        if field.data in club_names:
            raise ValidationError("Club Name already taken")
