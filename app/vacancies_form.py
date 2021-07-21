from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class VacancySearch(FlaskForm):
    search_term = StringField(validators=[DataRequired()])
    search_button = SubmitField("Search")

