import sqlite3
import csv
import requests
import lxml.html as lh


class RolesDatabase:
    roles_db = sqlite3.connect('app/databases/roles.db', check_same_thread=False)
    roles_db_cursor = roles_db.cursor()

    def role_database_initialise(self):
        self.roles_db.execute("""CREATE TABLE IF NOT EXISTS roles (
            job_role TEXT,
            rank INTEGER,
            rank_change INTEGER,
            median_salary INTEGER,
            median_salary_change REAL,
            historical INTEGER,
            live_job_count INTEGER
        )""")

    def del_all_roles(self):
        self.roles_db_cursor.execute("DELETE FROM roles")
        self.roles_db.commit()

    def add_role(self, job_role, rank, rank_change, median_salary, median_salary_change, historical,
                 live_job_count):
        self.roles_db_cursor.execute("INSERT INTO roles VALUES (?, ?, ?, ?, ?, ?, ?)",
                                     (job_role, rank, rank_change, median_salary, median_salary_change, historical,
                                      live_job_count))
        self.roles_db.commit()

    def remove_role(self, job_role):
        self.roles_db_cursor.execute("DELETE FROM roles WHERE job_role='{}'".format(job_role))
        self.roles_db.commit()

    def role_scrap_to_db(self):
        try:
            request = requests.get("https://www.itjobswatch.co.uk/")
            doc = lh.fromstring(request.content)  # initial scraping from URL
            tr_elements = doc.xpath('//tr')[
                          4:54]  # top 50 job scraped w/o headers. Remark: change 4->3 to incl. headers

            # Delete previous entries
            self.del_all_roles()
            # lambda functions
            integer = lambda x: -int(x.replace('-', '')) if '-' in x else int(x.replace('+', ''))
            rational = lambda x: -float(x.replace('-', '')) if '-' in x else float(x.replace('+', ''))
            dash_check = lambda x: '0' if x == '-' else x
            abridge = lambda x: int(x[0:x.find(' ')].replace(',', ''))

            for items in tr_elements:  # extracts elements from scraped site data
                self.add_role(items[0].text_content(),
                              int(items[1].text_content().replace(',', '')),  # Rank
                              integer(items[2].text_content().replace(',', '')),  # Rank Change
                              int(items[3].text_content().replace(',', '').replace('£', '')),  # Median Salary
                              rational(dash_check(items[4].text_content()).replace(',', '').replace('%', '')),  # MSC
                              int(abridge(items[5].text_content())),  # Historical Job Ads
                              int(items[6].text_content().replace(',', '')))  # Job Vacancies
        except Exception as e:
            print(e)
    
    # # Redundant code as view_sorted_roles > view_role
    # def view_role(self):
    #     self.roles_db_cursor.execute("SELECT * FROM roles")
    #     all_roles = self.roles_db_cursor.fetchall()
    #     return all_roles

    def view_sorted_roles(self, category, sort_order, is_auth):
        self.roles_db_cursor.execute("SELECT * FROM roles ORDER BY {} {}".format(category, sort_order))
        if is_auth:
            all_roles = self.roles_db_cursor.fetchall()
        else:
            all_roles = self.roles_db_cursor.fetchmany(5)
        return all_roles

    def view_selected_role(self, job_role):
        self.roles_db_cursor.execute("SELECT * FROM roles WHERE job_role='{}'".format(job_role))
        data = self.roles_db_cursor.fetchone()
        return [data]


    def export_to_csv(self, file_path):
        # Need to add error handling +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        self.roles_db_cursor.execute("select * from roles")
        with open(file_path, "w") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",", lineterminator='\n')
            csv_writer.writerow([i[0] for i in self.roles_db_cursor.description])
            csv_writer.writerows(self.roles_db_cursor)

        # --------------------------------------------------------------------------------------------------
        # roles_db = sqlite3.connect('app/databases/roles.db', check_same_thread=False)
        # roles_db_cursor = roles_db.cursor()
        # roles_db_cursor.execute("SELECT * FROM roles")
        # result = roles_db_cursor.fetchall()
        # output = io.StringIO()
        # writer = csv.writer(output)
        #
        # line = ['Role, Rank, Rank Change, Median Salary, Median Salary Change, Historical, Live Job Count']
        # writer.writerow(line)
        #
        # for row in result:
        #     line = row['job_role'] + ',' + row['rank'] + ',' + row['rank_change'] + ',' + row['median_salary'] + ',' + row['median_salary_change'] + ',' + row['historical']  + ',' + row['live_job_count']
        #     writer.writerow(line)
        #
        # output.seek(0)
        # --------------------------------------------------------------------------------------------------

    def search_role(self, category, sort_order, is_auth, data):
        constructed_query = "%" + data + "%"
        self.roles_db_cursor.execute("SELECT * FROM roles WHERE job_role LIKE (?) ORDER BY {} {}".format(category, sort_order), [constructed_query])
        if is_auth:
            query_roles = self.roles_db_cursor.fetchall()
        else:
            query_roles = self.roles_db_cursor.fetchmany(5)
        return query_roles
"""
        constructed_query = "%" + search_form.search_term.data + "%"
        roles_db_cursor.execute("SELECT * FROM roles WHERE job_role LIKE (?)", [constructed_query])
        data = roles_db_cursor.fetchall()

The following is temp code for development purposes.

# Create the database
RolesDatabase().role_database_initialise() # working 17/07/21 19:24

# Add to the database manually
RolesDatabase().add_role("Agile Software Development", 1, 0, 60_000, 4.34, 33_866, 5_983) # working 17/07/21 19:24
RolesDatabase().add_role("Developer", 2, 0, 55_000, 4.76, 29_478, 6_977)
RolesDatabase().add_role("Social Skills", 3, 1, 52_500, 3.20, 24_898, 5_726)

# Remove to the database manually
RolesDatabase().remove_role("Agile Software Development") # working 17/07/21 19:24

# Checking sorting 
print(RolesDatabase().view_sorted_roles('rank'))
print(RolesDatabase().view_sorted_roles('live_job_count'))

# Checking csv conversion
RolesDatabase().export_to_csv()

# Checking scrapper 
RolesDatabase().role_scrap_to_db()

"""

RolesDatabase().role_database_initialise()

