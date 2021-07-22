
from unittest.mock import MagicMock
import unittest
import sqlite3


class DataBaseClass:

    def __init__(self):
        print('initialising database class')
        self.connection = sqlite3.connect('test_database')


    def add_role(self, job_role, rank, rank_change, median_salary, median_salary_change, historical,
                 live_job_count):
        self.connection = sqlite3.connect('test_database')
        self.cursor = self.connection.cursor()
        self.cursor.execute("DELETE FROM roles")
        self.connection.execute("""CREATE TABLE IF NOT EXISTS roles (
                            job_role TEXT,
                            rank INTEGER,
                            rank_change INTEGER,
                            median_salary INTEGER,
                            median_salary_change REAL,
                            historical INTEGER,
                            live_job_count INTEGER
                        )""")
        self.connection.cursor().execute("INSERT INTO roles VALUES (?, ?, ?, ?, ?, ?, ?)",
                                         (job_role, rank, rank_change, median_salary, median_salary_change, historical,
                                          live_job_count))
        self.connection.commit()


class MyTests(unittest.TestCase):

    def test_sqlite3_connect_success(self):
        sqlite3.connect = MagicMock(return_value='connection succeeded')
        dbc = DataBaseClass()
        sqlite3.connect.assert_called_with('test_database')
        self.assertEqual(dbc.connection, 'connection succeeded')

    def test_add_role(self):
        dbc = DataBaseClass()
        dbc.add_role('test_role', '1', '0', '50000', '0', '300', '2500')
        dbc.cursor.execute("SELECT rowid FROM roles WHERE job_role = job_role")
        data = dbc.cursor.fetchall()
        self.assertEqual([(1,)], data)  # expects added role to be in row 1
