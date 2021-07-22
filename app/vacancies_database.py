import os
import sqlite3
import csv
import requests
import lxml.html as lh
import pandas as pd
import datetime

class VacanciesDatabase:
    vacancy_db = sqlite3.connect('app/databases/vacancies.db', check_same_thread=False)
    vacancy_db_cursor = vacancy_db.cursor()

    def vacancy_database_initialise(self):
        for i in ['vacancies', 'rec_vacancies']:
            self.vacancy_db.execute("""CREATE TABLE IF NOT EXISTS {} (
                job_name TEXT,
                location TEXT,
                company TEXT,
                job_details TEXT,
                salary TEXT,
                time_posted TEXT
            )""".format(i))
            self.vacancy_db.commit()

    def del_all_vacancies(self):
        self.vacancy_db_cursor.execute("DELETE FROM vacancies")
        self.vacancy_db.commit()

    def add_vacancy(self, job_name, location, company, job_details, salary, time_posted):
        self.vacancy_db_cursor.execute("INSERT INTO vacancies VALUES (?, ?, ?, ?, ?, ?)",
                                       (job_name, location, company, job_details, salary, time_posted))
        self.vacancy_db.commit()

    def remove_vacancy(self, job_name):
        self.vacancy_db_cursor.execute("DELETE FROM vacancies WHERE job_name='{}'".format(job_name))
        self.vacancy_db.commit()

    # def del_all_vacancies(self):
    #     self.vacancy_db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    #     tables = self.vacancy_db_cursor.fetchall()
    #     for table_name in tables:
    #         table_name = table_name[0]
    #         self.vacancy_db_cursor.execute("DROP TABLE IF EXISTS {}".format(table_name))
    #         self.vacancy_db.commit()
    #
    # def view_sorted_vacancies(self, job_role):
    #     job_role = job_role.replace(" ", "_").lower()  # Need to remove/replace all whitespaces for table name
    #     self.vacancy_db_cursor.execute("SELECT * FROM {}".format(job_role))
    #     all_jobs = self.vacancy_db_cursor.fetchall()
    #     # need to return list in list so view_all_vacancies doesn't need unpacking
    #     return [all_jobs]
    #
    # def view_all_vacancies(self):
    #     self.vacancy_db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    #     tables = self.vacancy_db_cursor.fetchall()
    #     all_jobs = []
    #     for table_name in tables:
    #         table_name = table_name[0]
    #         self.vacancy_db_cursor.execute("SELECT * FROM {}".format(table_name))
    #         all_jobs.append(self.vacancy_db_cursor.fetchall())
    #     return all_jobs

    def vacancies_scrap_to_db(self):
        try:
            request = requests.get("https://www.itjobswatch.co.uk/IT-Jobs")
            doc = lh.document_fromstring(request.content)
            vacancies = doc.find_class('job')  # getting all job data entries from site
            vacancy_list = []
            for i in range(len(vacancies)):
                vac = str(vacancies[i].text_content())  # extracting text content from html files
                vac = os.linesep.join([s for s in vac.splitlines() if s.strip()])  # removing blank lines
                vac = vac[36:]  # blank space at the beginning of each entry
                vac = vac.split("\n                                    ")  # separator from scraped table entries
                vacancy_list.append(vac)

            for item in vacancy_list:
                item.insert(1,
                            item[1].split(' - ')[0])  # these 3 lines split the location-company string into 2 separate
                item.insert(2, item[2].split(' - ')[1])  # may be a simpler way but this works for now
                item.pop(3)
                if len(item) == 5:
                    item.insert(4, "None")  # adding a None salary if not listed

            data_df = pd.DataFrame(vacancy_list, columns=["job_name", "location", "company", "job_details",
                                                          "salary", "time_posted"])

            pd.set_option("display.max_rows", None, "display.max_columns", None)

            self.del_all_vacancies()

            for i in data_df.index:
                self.add_vacancy(data_df['job_name'][i],
                                 data_df['location'][i],
                                 data_df['company'][i],
                                 data_df['job_details'][i],
                                 data_df['salary'][i],
                                 data_df['time_posted'][i]
                                 )
        except Exception as e:
            print(e)

    def view_vacancies(self):
        all_vacancies = []
        for i in ['vacancies','rec_vacancies']:
            self.vacancy_db_cursor.execute("SELECT * FROM {}".format(i))
            all_vacancies += self.vacancy_db_cursor.fetchmany(20)
        return all_vacancies

    def search_vacancy(self, data):
        constructed_query = "%" + data + "%"
        self.vacancy_db_cursor.execute("SELECT * FROM vacancies WHERE job_name LIKE (?)", [constructed_query])
        query_roles = self.vacancy_db_cursor.fetchmany(5)
        self.vacancy_db_cursor.execute("SELECT * FROM rec_vacancies WHERE job_name LIKE (?)", [constructed_query])
        query_roles += self.vacancy_db_cursor.fetchmany(5)
        return query_roles


    def recruiter_add_vacancy(self, job_name, location, company, job_details, salary):
        now = datetime.datetime.now()
        posted = now.strftime("%d %B %Y")
        self.vacancy_db_cursor.execute("INSERT INTO rec_vacancies VALUES (?, ?, ?, ?, ?, ?)",
                                       (job_name, location, company, job_details, salary, posted))
        self.vacancy_db.commit()

    def recruiter_remove_vacancy(self, job_name):
        self.vacancy_db_cursor.execute("DELETE FROM rec_vacancies WHERE job_name='{}'".format(job_name))
        self.vacancy_db.commit()


"""

The following is temp code for development purposes.

VacanciesDatabase().vacancies_scrap_to_db()


"""
VacanciesDatabase().vacancy_database_initialise()
# VacanciesDatabase().recruiter_add_vacancy('dev', 'brum', 'sparta', 'blah', 'Salary: £0', 'Posted: Now')
# VacanciesDatabase().recruiter_remove_vacancy('dev')
