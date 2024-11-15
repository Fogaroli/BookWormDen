from flask_wtf import FlaskForm
from sqlalchemy import Integer
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
    NumberRange,
    ValidationError,
)


class UserAddForm(FlaskForm):
    """Form for user registration."""

    first_name = StringField("First name", validators=[DataRequired(), Length(max=50)])
    last_name = StringField("Last name", validators=[DataRequired(), Length(max=50)])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])

    def validate_username(form, field):
        if " " in field.data or "-" in field.data:
            raise ValidationError("Username must not contain spaces or dashes.")


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
