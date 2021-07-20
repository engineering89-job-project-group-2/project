import os
import sqlite3
import csv
import requests
from lxml import html

request = requests.get("https://www.itjobswatch.co.uk/IT-Jobs")
sourceCode = request.content

htmlElem = html.document_fromstring(sourceCode)
vacancies = htmlElem.find_class('job')  # getting all job data entries from site
vacancy_list = []
for i in range(len(vacancies)):
    vac = str(vacancies[0].text_content())  # extracting text content from html files
    vac = os.linesep.join([s for s in vac.splitlines() if s.strip()])  # removing blank lines
    vac = vac[36:]  # blank space at the beginning of each entry
    vac = vac.split("\n                                    ")  # separator from scraped table entries
    vacancy_list.append(vac)
print(vacancy_list)
# title_list = []
# job_title = htmlElem.find_class('jobTitle')
# for i in range(len(job_title)):
#     title = str(job_title[i].text_content())
#     title = os.linesep.join([s for s in title.splitlines() if s.strip()])  # removing blank lines from string
#     title = title[36:]  # 36 blanks spaces at start of each line
#     title_list.append(title)
# print(title_list)
# location_company = htmlElem.find_class('jobDetails jobDetailsTop')
# job_description = htmlElem.find_class('jobDescription')
# salary_posted = htmlElem.find_class('jobDetails')
