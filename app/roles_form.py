from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField
from wtforms.validators import DataRequired


class RolesForm(FlaskForm):
    options = ['Alphabetical',
               'Rank',
               'Rank Change',
               'Median Salary',
               'Median Salary Change',
               'Historical Job Ads',
               'Job Vacancies'
               ]
    role_filter = SelectField(choices=options, validators=[DataRequired()])
    sort = SubmitField('Sort')


class RoleSearch(FlaskForm):
    search_term = StringField(validators=[DataRequired()])
    search_button = SubmitField("Search")
