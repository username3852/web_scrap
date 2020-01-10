import requests
from bs4 import BeautifulSoup
import csv

source = "http://mohp.gov.np/eng/health-institutions/government/central-hospitals"

def get_info(url):
    response = requests.get(source)
    soup = BeautifulSoup(response.content, 'lxml')
    tables = soup.find_all('table', class_='w3-table w3-striped')
    table = tables[0]
    all_rows = table.find_all('tr')
    head_columns, data_rows = all_rows[0], all_rows[1:]
    new_columns = [td.text.split('\n')[1] for td in head_columns.find_all('td')]
    new_rows = [[td.text.split('\n')[1] for td in row.find_all('td') ]for row in data_rows ]
    return new_columns, new_rows

def zipped_data(**kwargs):
    columns = kwargs.get('columns')
    rows= kwargs.get('rows')
    return [dict(zip(columns, rows)) for row in rows]

def write_to_csv(filename, datas):
    with open(filename, 'w') as write_file:
        writer = csv.DictWriter(write_file, fieldnames=datas[0].keys())
        writer.writeheader()
        writer.writerows(datas)

columns, rows = get_info(source)
datas = zipped_data(columns=columns, rows=rows)
write_to_csv("Ministry_of_hospitals.csv", datas)