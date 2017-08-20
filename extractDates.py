from lxml import html
from date import date
import requests
def extractDates():
    page = requests.get('https://sydney.edu.au/bin/students/dates/c/dc.key-dates|jcrcontent|par-zone3|dates_content_page.json').json()
    for key in page:
        page[key]['startDate'] = date(page[key]['startDate'])
        page[key]['endDate'] = date(page[key]['endDate'])
    return page
print(extractDates())
