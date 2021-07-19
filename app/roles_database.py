import sqlite3
import csv
import datetime
from flask import send_file, Response

class RolesDatabase:
    roles_db = sqlite3.connect('app/databases/roles.db', check_same_thread=False)
    roles_db_cursor = roles_db.cursor()

    def role_database_initialise(self):
        self.roles_db.execute("""CREATE TABLE IF NOT EXISTS roles (
            job_role TEXT,
            rank INTEGER,
            rank_change REAL,
            median_salary INTEGER,
            median_salary_change REAL,
            historical INTEGER,
            live_job_count INTEGER
        )""")

    def add_role(self, job_role, rank, rank_change, median_salary, median_salary_change, historical,
                 live_job_count):
        self.roles_db_cursor.execute("INSERT INTO roles VALUES (?, ?, ?, ?, ?, ?, ?)",
                                     (job_role, rank, rank_change, median_salary, median_salary_change, historical,
                                      live_job_count))
        self.roles_db.commit()

    def remove_role(self, job_role):
        self.roles_db_cursor.execute("DELETE FROM roles WHERE job_role='{}'".format(job_role))
        self.roles_db.commit()

    # # Redundant code as view_sorted_roles > view_role
    # def view_role(self):
    #     self.roles_db_cursor.execute("SELECT * FROM roles")
    #     all_roles = self.roles_db_cursor.fetchall()
    #     return all_roles

    def view_sorted_roles(self, category, sort_order):
        self.roles_db_cursor.execute("SELECT * FROM roles ORDER BY {} {}".format(category, sort_order))
        all_roles = self.roles_db_cursor.fetchall()
        return all_roles

    def export_to_csv(self):
        self.roles_db_cursor.execute("SELECT * FROM roles")
        now = datetime.datetime.now
        path = "generated/roles_{}.csv".format(now.strftime("%Y%m%d%H%m%s"))
        with open(path, "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",", lineterminator='\n')
            csv_writer.writerow([i[0] for i in self.roles_db_cursor.description])
            csv_writer.writerows(self.roles_db_cursor)
        return path
        # need to add download part
        # send_file(path, as_attachment=True)


"""

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

"""