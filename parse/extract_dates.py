from lxml import html
from date import date
import requests
def extract_dates():
    page = requests.get('https://sydney.edu.au/bin/students/dates/c/dc.key-dates|jcrcontent|par-zone3|dates_content_page.json').json()
    for key in page:
        page[key]['start_date'] = date(page[key]['start_date'])
        page[key]['end_date'] = date(page[key]['end_date'])
    return page
print(extract_dates())
