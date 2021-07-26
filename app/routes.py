import os
import sqlite3

from flask import render_template, flash, redirect, url_for, session, current_app, request
from app import flask_app
from app.login_form import LoginForm, RegisterForm
from app.login_database import LoginDatabase
from app.role_scrap import RolesScrap
from app.vacancies_database import VacanciesDatabase
from app.vacancies_form import VacancySearch
from app.roles_database import RolesDatabase
from app.roles_form import RolesForm, RoleSearch
from flask import send_file
from app.login_form import RecruiterVacanciesForm

@flask_app.route('/index')
@flask_app.route('/')
def index():
    return render_template('index.html', title='Home')


@flask_app.route('/login/', methods=['GET', 'POST'])
def login():
    try:
        if 'username' in session:
            return redirect(url_for('index'))
    except Exception as e:
        print(e)

    form = LoginForm()
    if form.validate_on_submit():
        db = LoginDatabase()
        db.users_db_cursor.execute("SELECT * FROM users WHERE username = (?)", [form.username.data])
        try:
            user = list(db.users_db_cursor.fetchone())
        except:
            flash("Invalid username or password")
            return redirect(url_for('login'))
        if not db.compare(form.username.data, form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        session['username'] = form.username.data
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@flask_app.route('/register/', methods=['GET', 'POST'])
def register():
    try:
        if 'username' in session:
            return redirect(url_for('index'))
    except Exception as e:
        print(e)

    form = RegisterForm()
    if form.validate_on_submit():
        db = LoginDatabase()
        db.new_user(str(form.email.data), str(form.username.data), str(form.password.data))
        flash("User registration complete!")
    return render_template('register.html', title='Register a new user', form=form)


@flask_app.route('/logout/')
def logout():
    session.pop('admin', None)
    session.pop('username', None)
    return redirect(url_for('index'))


@flask_app.route('/roles/', methods=['GET', 'POST'])
def roles():
    search_form = RoleSearch(request.form)

    filter_form = RolesForm()
    category = 'rank'
    sort_order = 'ASC'
    if filter_form.validate_on_submit():
        RolesDatabase().role_scrap_to_db()
        # python switch lol
        # need to figure out how to order; is bigger always better? ASC = ascending, DESC = descending
        if filter_form.role_filter.data == 'Alphabetical':
            category = 'job_role'
            sort_order = 'ASC'
        elif filter_form.role_filter.data == 'Rank Change':
            category = 'rank_change'
            sort_order = 'DESC'
        elif filter_form.role_filter.data == 'Median Salary':
            category = 'median_salary'
            sort_order = 'DESC'
        elif filter_form.role_filter.data == 'Median Salary Change':
            category = 'median_salary_change'
            sort_order = 'DESC'
        elif filter_form.role_filter.data == 'Historical Job Ads':
            category = 'historical'
            sort_order = 'DESC'
        elif filter_form.role_filter.data == 'Job Vacancies':
            category = 'live_job_count'
            sort_order = 'DESC'
        else:
            category = 'rank'
            sort_order = 'ASC'
        flash('{}'.format(filter_form.role_filter.data))

    is_auth = True if 'username' in session else False
    data = RolesDatabase().view_sorted_roles(category, sort_order, is_auth)

    if search_form.validate_on_submit():
        data = RolesDatabase().search_role(category, sort_order, is_auth, search_form.search_term.data)
    return render_template('roles.html', title='Roles', form=filter_form, search=search_form, data=data)




@flask_app.route('/vacancies/', methods=['GET', 'POST'])
def vacancies():
    # If not logged in, return user to index
    try:
        if 'username' not in session:
            return redirect(url_for('index'))
    except Exception as e:
        print(e)

    VacanciesDatabase().vacancies_scrap_to_db()

    search_form = VacancySearch()
    data = VacanciesDatabase().view_vacancies()

    if search_form.validate_on_submit():
        data = VacanciesDatabase().search_vacancy(search_form.search_term.data)

    return render_template('vacancies.html', title='Vacancies', search=search_form, data=data)


@flask_app.route('/download/', methods=['GET'])
def download_csv():
    file_name = 'roles_download.csv'
    RolesDatabase().export_to_csv(f'app/outputs/{file_name}')
    return send_file(f"outputs/{file_name}", mimetype='text/csv', as_attachment=True)


@flask_app.route('/recruiter/', methods=['GET', 'POST'])
def recruiter():
    try:
        if 'username' not in session:
            return redirect(url_for('login'))
    except Exception as e:
        print(e)

    form = RecruiterVacanciesForm()

    if form.validate_on_submit():
        VacanciesDatabase().recruiter_add_vacancy(form.job_name.data,
                                                  form.location.data,
                                                  form.company.data,
                                                  form.job_details.data,
                                                  form.salary.data
                                                  )

    return render_template('recruiter.html', title='Add a Job Vacancy', form=form)


@flask_app.route("/roles/<role>", methods=['GET'])
def render_role(role):
    data = RolesDatabase().view_selected_role(role.replace('_', ' '))
    scrap = RolesScrap().scrap(role)
    cdata = RolesDatabase().view_sorted_roles('job_role', 'ASC', True)
    labels = [row[0] for row in cdata]
    values = [row[5] for row in cdata]
    colour = []
    for row in cdata:
        if row[0] == role.replace('_', ' '):
            colour.append("#81B811")
        else:
            colour.append("#bbb")

    return render_template("view.html", role=role, data=data, scrap=scrap, labels=labels, values=values, colour=colour)


