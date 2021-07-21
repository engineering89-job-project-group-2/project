import os
import sqlite3
import csv
import pandas as pd
import requests
from lxml import html

request = requests.get("https://www.itjobswatch.co.uk/IT-Jobs")
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
    item.insert(1, item[1].split(' - ')[0])  # these 3 lines split the location-company string into 2 separate
    item.insert(2, item[2].split(' - ')[1])  # may be a simpler way but this works for now
    item.pop(3)
    if len(item) == 5:
        item.insert(4, "None")  # adding a None salary if not listed

# print(vacancy_list)
data_df = pd.DataFrame(vacancy_list, columns=["Job Title", "Location", "Company", "Job Details",
                                              "Salary(if available)", "Time Posted"])
print(data_df)

# create SQL database: Job Title, Location/Company, Job Description, Salary if there
