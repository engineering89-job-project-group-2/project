from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
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
    submit = SubmitField('Sort')


class RolesDownload(FlaskForm):
    submit = SubmitField('Download .csv')
