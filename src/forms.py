from flask_wtf import FlaskForm
from sqlalchemy import Integer
from wtforms import StringField, PasswordField, DateField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, Optional


class UserAddForm(FlaskForm):
    """Form for user registration."""

    first_name = StringField("First name", validators=[DataRequired(), Length(max=50)])
    last_name = StringField("Last name", validators=[DataRequired(), Length(max=50)])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])


class readStatisticsForm(FlaskForm):
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
