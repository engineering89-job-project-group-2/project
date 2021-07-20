from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired #, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField()


class RegisterForm(FlaskForm):
    first_name = StringField(validators=[DataRequired()])
    last_name = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired()])
#   email = StringField(validators=[DataRequired(), Email()])
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    confirm_password = PasswordField(validators=[DataRequired()])
#   confirm_password = PasswordField(validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField()
