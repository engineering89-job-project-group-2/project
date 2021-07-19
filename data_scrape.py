import requests
import lxml.html as lh
import pandas as pd
import sqlite3
from sqlite3 import Error

scrape = requests.get("https://www.itjobswatch.co.uk/")
doc = lh.fromstring(scrape.content)  # initial scraping from URL

# top 50 job scraped with header as well
tr_elements = doc.xpath('//tr')[3:54]  # selects table rows to scrape

row = []
j = 0
# For each row, store each first element (header) and an empty list
for items in tr_elements:  # extracts elements from scraped site data
    for t in items:
        j += 1
        name = t.text_content()  # text content of site
        row.append(name)
# print(row)  # returned in one list


def create_rows(seq, num):  # function to split list into a number of sub lists
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


data = create_rows(row, 51)  # splits one long list into on list per row (51 rows)
data.pop(0)  # removes header from list as it is added below
data_df = pd.DataFrame(data, columns=['Description', 'Rank (last 6 months', 'Rank Change YoY', 'Median Salary',
                                      'Median Salary Change YOY', 'Historical Permanent Ads', 'Live Jobs'])
# creates dataframe from list
# print(data_df)


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_connection(r"/Users/Tom1/Documents/Sparta/Week6_project/flask/app/databases/data_scrape.db")
