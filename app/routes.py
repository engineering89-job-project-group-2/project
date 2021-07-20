import sqlite3

from flask import render_template, flash, redirect, url_for, session, request
from app import flask_app
from app.login_form import LoginForm, RegisterForm
from app.login_database import LoginDatabase
from app.vacancies_database import VacanciesDatabase
from app.vacancies_form import VacancyForm
from app.roles_database import RolesDatabase
from app.roles_form import RolesForm, RolesDownload, RoleSearch
from flask import send_file


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
        if user[3] == 'admin':
            session['admin'] = True
        flash('Logged in successfully')
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
        db.new_user(int(form.staff_id.data), str(form.username.data), str(form.password.data), str(form.role.data))
        flash("User registration complete!")
    return render_template('register.html', title='Register a new user', form=form)


@flask_app.route('/logout/')
def logout():
    session.pop('admin', None)
    session.pop('username', None)
    return redirect(url_for('index'))


@flask_app.route('/roles/', methods=['GET', 'POST'])
def roles():
    form = RolesForm()
    download = RolesDownload()
    category = 'rank'
    sort_order = 'ASC'
    # if download.validate_on_submit():
    #     flash('Hello')
    if form.validate_on_submit():
        RolesDatabase().role_scrap_to_db()
        # python switch lol
        # need to figure out how to order; is bigger always better? ASC = ascending, DESC = descending
        if form.role_filter.data == 'Alphabetical':
            category = 'job_role'
            sort_order = 'ASC'
        elif form.role_filter.data == 'Rank Change':
            category = 'rank_change'
            sort_order = 'DESC'
        elif form.role_filter.data == 'Median Salary':
            category = 'median_salary'
            sort_order = 'DESC'
        elif form.role_filter.data == 'Median Salary Change':
            category = 'median_salary_change'
            sort_order = 'DESC'
        elif form.role_filter.data == 'Historical Job Ads':
            category = 'historical'
            sort_order = 'DESC'
        elif form.role_filter.data == 'Job Vacancies':
            category = 'live_job_count'
            sort_order = 'DESC'
        else:
            category = 'rank'
            sort_order = 'ASC'

        flash('{}'.format(form.role_filter.data))
    return render_template('roles.html', title='Roles', form=form,
                           data=RolesDatabase().view_sorted_roles(category, sort_order), download=download)


@flask_app.route('/search/', methods=['GET', 'POST'])
def search():
    roles_db = sqlite3.connect('app/databases/roles.db', check_same_thread=False)
    roles_db_cursor = roles_db.cursor()
    search_form = RoleSearch(request.form)
    if search_form.validate_on_submit():
        constructed_query = "%" + search_form.search_term.data + "%"
        roles_db_cursor.execute("SELECT * FROM roles WHERE job_role LIKE (?)", [constructed_query])
        query_roles = roles_db_cursor.fetchall()
        return render_template('search.html', title='Search', form=search_form, data=query_roles)
    return render_template('search.html', title='Search', form=search_form, data=RolesDatabase().view_sorted_roles('job_role', 'ASC'))


@flask_app.route('/vacancies/', methods=['GET', 'POST'])
def vacancies():
    # If not logged in, return user to index
    try:
        if 'username' not in session:
            return redirect(url_for('index'))
    except Exception as e:
        print(e)

    form = VacancyForm()
    data = VacanciesDatabase().view_all_vacancies()
    if form.validate_on_submit():
        if form.job_filter.data != 'All':
            flash('Added filter for {}'.format(form.job_filter.data))
            data = VacanciesDatabase().view_sorted_vacancies(form.job_filter.data)

    return render_template('vacancies.html', title='Vacancies', form=form, data=data)


@flask_app.route('/download')
def download_csv():
    return send_file('outputs/download.csv', mimetype='text/csv', as_attachment=True)
