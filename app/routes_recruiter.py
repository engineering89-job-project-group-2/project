import os
import sqlite3

from flask import render_template, flash, redirect, url_for, session, current_app, request
from app import flask_app
from app.recruiter_upload_form import RecruiterVacanciesForm
from app.login_form import LoginForm, RegisterForm
from app.login_database import LoginDatabase
from app.vacancies_database import VacanciesDatabase
from app.vacancies_form import VacancyForm
from app.roles_database import RolesDatabase
from app.roles_form import RolesForm, RolesDownload, RoleSearch
from flask import send_file



@flask_app.route('/recruiter_upload/', methods=['GET', 'POST'])
def recruiter_upload():
    try:
        if 'username' in session:
            return redirect(url_for('index'))
    except Exception as e:
        print(e)

    # form = RecruiterVacanciesForm()
    # if form.validate_on_submit():
    #     db = LoginDatabase()
    #     db.new_user(int(form.staff_id.data), str(form.username.data), str(form.password.data), str(form.role.data))
    #     flash("User registration complete!")
    # return render_template('register.html', title='Register a new user', form=form)
    #
