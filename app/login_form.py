from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField()


class RegisterForm(FlaskForm):
    first_name = StringField(validators=[DataRequired()])
    last_name = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired()])
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
<<<<<<< Updated upstream
    confirm_password = PasswordField(validators=[DataRequired()])
=======
    #confirm_password = PasswordField(validators=[DataRequired()])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField()


class RecruiterVacanciesForm(FlaskForm):
    job_name = StringField(validators=[DataRequired(), Length(min=1, max=30)])
    company = StringField(validators=[DataRequired()])
    location = StringField(validators=[DataRequired()])
    salary = StringField(validators=[DataRequired()])
    job_type = StringField(validators=[DataRequired()])
    deadline = StringField(validators=[DataRequired()])
>>>>>>> Stashed changes
    submit = SubmitField()
