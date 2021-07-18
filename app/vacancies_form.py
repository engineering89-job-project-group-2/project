from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

from app.vacancies_database import VacanciesDatabase


class VacancyForm(FlaskForm):
    db = VacanciesDatabase()
    db.vacancy_db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = db.vacancy_db_cursor.fetchall()
    all_jobs = ['All']
    for table_name in tables:
        all_jobs.append(table_name[0].replace("_", " ").title())

    job_filter = SelectField(choices=all_jobs, validators=[DataRequired()])
    submit = SubmitField()
