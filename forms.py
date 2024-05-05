from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length

class NewUserForm(FlaskForm):
    """Form for signing up a new user"""
    
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])

class LogUserIn(FlaskForm):
    """Authentication form for existing user"""
    # Maybe can reuse NewUserForm and just rename it?

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])

class ChangePasswordForm(FlaskForm):
    """Enter existing password then new password twice"""

    oldPassword = PasswordField("OldPassword", validators=[DataRequired()])
    newPassword1 = PasswordField("NewPassword1", validators=[DataRequired(), Length(min=6)])
    newPassword2 = PasswordField("NewPassword2", validators=[DataRequired(), Length(min=6)])