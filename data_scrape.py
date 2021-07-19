import requests
import lxml.html as lh
import pandas as pd

scrape = requests.get("https://www.itjobswatch.co.uk/")
doc = lh.fromstring(scrape.content)

# top 50 job scraped with header as well
tr_elements = doc.xpath('//tr')[3:54]

row = []
j = 0
# For each row, store each first element (header) and an empty list
for items in tr_elements:
    for t in items:
        j += 1
        name = t.text_content()
        row.append(name)
print(row)


def create_rows(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


data = create_rows(row, 51)
data.pop(0)
data_df = pd.DataFrame(data, columns=['Description', 'Rank (last 6 months', 'Rank Change YoY', 'Median Salary',
                                      'Median Salary Change YOY', 'Historical Permanent Ads', 'Live Jobs'])
print(data_df)
