import sqlite3
import requests
import os
from lxml import html


class VacanciesDatabase:
    vacancy_db = sqlite3.connect('app/databases/vacancies.db', check_same_thread=False)
    vacancy_db_cursor = vacancy_db.cursor()
# "Job Title", "Location", "Company", "Job Details", "Salary(if available)", "Time Posted" - Headings from scrape

    def vacancy_database_initialise(self):
        self.vacancy_db_cursor.execute("""CREATE TABLE IF NOT EXISTS {} (
                job_title text,
                location text,
                company text,
                job_details text,
                salary text,
                time_posted text
            )""")

    def vacancy_scrap_to_db(self):
        try:
            request = requests.get("https://www.itjobswatch.co.uk/IT-Jobs")
            # doc = lh.fromstring(request.content)  # initial scraping from URL
            # tr_elements = doc.xpath('//tr')[
            #               4:54]  # top 50 job scraped w/o headers. Remark: change 4->3 to incl. headers

            # Delete previous entries
            self.del_all_roles()
            sourceCode = request.content

            htmlElem = html.document_fromstring(sourceCode)
            vacancies = htmlElem.find_class('job')  # getting all job data entries from site
            vacancy_list = []
            for i in range(len(vacancies)):
                vac = str(vacancies[i].text_content())  # extracting text content from html files
                vac = os.linesep.join([s for s in vac.splitlines() if s.strip()])  # removing blank lines
                vac = vac[36:]  # blank space at the beginning of each entry
                vac = vac.split("\n                                    ")  # separator from scraped table entries
                vacancy_list.append(vac)
            # print(vacancy_list)
            for item in vacancy_list:
                item.insert(1, item[1].split(' - ')[0])  # these lines split the location-company string into 2 separate
                item.insert(2, item[2].split(' - ')[1])  # may be a simpler way but this works for now
                item.pop(3)  # removes original location-company
                if len(item) == 5:
                    item.insert(4, "Not Available")  # adding n/a salary if not listed
                self.add_vacancy(str(item[0]),  # Job Title
                                 str(item[1]),  # Location
                                 str(item[2]),  # Company
                                 str(item[3]),  # Job Details
                                 str(item[4]),  # Salary
                                 str(item[5]))  # Time Posted

            # print(vacancy_list)
            # data_df = pd.DataFrame(vacancy_list, columns=["Job Title", "Location", "Company", "Job Details",
            #                                               "Salary(if available)", "Time Posted"])

            # lambda functions
            # integer = lambda x: -int(x.replace('-', '')) if '-' in x else int(x.replace('+', ''))
            # rational = lambda x: -float(x.replace('-', '')) if '-' in x else float(x.replace('+', ''))
            # dash_check = lambda x: '0' if x == '-' else x
            # abridge = lambda x: int(x[0:x.find(' ')].replace(',', ''))
        #
        #     for items in tr_elements:  # extracts elements from scraped site data
        #         self.add_role(items[0].text_content(),
        #                       int(items[1].text_content().replace(',', '')),  # Rank
        #                       integer(items[2].text_content().replace(',', '')),  # Rank Change
        #                       int(items[3].text_content().replace(',', '').replace('£', '')),  # Median Salary
        #                       rational(dash_check(items[4].text_content()).replace(',', '').replace('%', '')),  # MSC
        #                       int(abridge(items[5].text_content())),  # Historical Job Ads
        #                       int(items[6].text_content().replace(',', '')))  # Job Vacancies
        except Exception as e:
            print(e)

    def add_vacancy(self, job_role, job_title, location, company, job_details, salary, time_posted):
        job_role = job_role.replace(" ", "_").lower()   # Need to remove/replace all whitespaces for table name
        self.vacancy_db_cursor.execute('INSERT INTO {} VALUES (?, ?, ?, ?, ?, ?)'.format(job_role),
                                       (job_title, location, company, job_details, salary, time_posted))
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

