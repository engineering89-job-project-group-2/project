import sqlite3


class VacanciesDatabase:
    vacancy_db = sqlite3.connect('app/databases/vacancies.db', check_same_thread=False)
    vacancy_db_cursor = vacancy_db.cursor()

    def add_vacancy(self, job_role, job_name, company, location, salary, job_type, deadline):
        job_role = job_role.replace(" ", "_").lower()   # Need to remove/replace all whitespaces for table name
        self.vacancy_db_cursor.execute("""CREATE TABLE IF NOT EXISTS {} ( 
            job_name text,
            company text, 
            location text, 
            salary INTEGER, 
            job_type text,
            deadline text
        )""".format(job_role))
        self.vacancy_db_cursor.execute('INSERT INTO {} VALUES (?, ?, ?, ?, ?, ?)'.format(job_role),
                                       (job_name, company, location, salary, job_type, deadline))
        self.vacancy_db.commit()

    def view_sorted_vacancies(self, job_role):
        job_role = job_role.replace(" ", "_").lower()   # Need to remove/replace all whitespaces for table name
        self.vacancy_db_cursor.execute("SELECT * FROM {}".format(job_role))
        all_jobs = self.vacancy_db_cursor.fetchall()
        # need to return list in list so view_all_vacancies doesn't need unpacking
        return [all_jobs]

    def view_all_vacancies(self):
        self.vacancy_db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.vacancy_db_cursor.fetchall()
        all_jobs = []
        for table_name in tables:
            table_name = table_name[0]
            self.vacancy_db_cursor.execute("SELECT * FROM {}".format(table_name))
            all_jobs.append(self.vacancy_db_cursor.fetchall())
        return all_jobs


"""

The following is temp code for development purposes.

# Add to the database manually
VacanciesDatabase().add_vacancy('Agile Software Development', 'Name of Job 1', 'Gravitas Recruitment Group Ltd', 'Portsmouth, Hampshire',
                                30_000, 'Permanent', '01-09-21')

VacanciesDatabase().add_vacancy('Developer', 'Name of Job 2', 'Rise Technical Recruitment Ltd', 'Cardiff',
                                50_000, 'Permanent', 'N/A')
                                

VacanciesDatabase().view_all_vacancies()

print(VacanciesDatabase().view_sorted_vacancies('Agile Software Development'))
"""
# VacanciesDatabase().add_vacancy('Agile Software Development', 'Name of Job 1', 'Gravitas Recruitment Group Ltd',
#                                 'Portsmouth, Hampshire',
#                                 30_000, 'Permanent', '01-09-21')
#
# VacanciesDatabase().add_vacancy('Developer', 'Name of Job 2', 'Rise Technical Recruitment Ltd', 'Cardiff',
#                                 50_000, 'Permanent', 'N/A')

