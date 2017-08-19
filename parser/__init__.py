import requests
from pprint import pprint
from bs4 import BeautifulSoup

def parse(course_code):
    pass  # hahahaha the parse function passes

def get_page(link):
    """
    this thing takes a link and shoves back some html shit
    """
    r = requests.get(link)
    r.raise_for_status()
    return r.content

def cusp(course_code):
    """
    Takes a course code and returns a list containing dictionary objects which represent courses.

    All ye who enter, beware. There are list comprehensions abroad.
    """
    return [{'assessment_number': x[0], 'name': x[1], 'is_group': x[2], 'weight': x[3], 'due_string': x[4]} for x in [[x.text.strip() for x in x.find_all('td')][:-1] for x in BeautifulSoup(get_page('https://cusp.sydney.edu.au/students/view-unit-page/alpha/' + course_code), 'html.parser').find(string="Assessment Methods:").parent.next_element.next_element.next_element.next_element.next_element.find_all('tr')][1:]]

def export(dictionary):
    pass  # should probably do something here

# This stuff runs when you run this file like `python3 __init__.py` (but not when you import it)
if __name__ == '__main__':
    while True:
        cusp(input('> '))
