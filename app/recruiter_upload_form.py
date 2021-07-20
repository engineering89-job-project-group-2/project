from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class recruiterVacanciesForm(FlaskForm):
    job_name = StringField(validators=[DataRequired(),Length(min=1, max=50)])
    company = StringField(validators=[DataRequired(), Length(min=1, max=30)])
    location = StringField(validators=[DataRequired(), Length(min=1, max=30)])
    salary = StringField(validators=[DataRequired(), Length(min=1, max=10)])
    job_type = StringField(validators=[DataRequired(), Length(min=1, max=50)])
    deadline = StringField(validators=[DataRequired(), Length(min=1, max=30)])
    submit = SubmitField()
