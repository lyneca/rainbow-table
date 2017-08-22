import requests
from pprint import pprint
from bs4 import BeautifulSoup

def parse(course_code):
    pass

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

def export(course_code):
    course = cusp(course_code)
    data = open("data/data.py", 'r+')
    globs = {}
    exec(data.read(), globs)
    data.close()
    data = open("data/data.py", 'w')
    globs['assessment'][course_code] = course
    data.write("assessment = "+str(globs['assessment']))
    data.close()

def get_assess_dict():
    data = open("data/data.py")
    empty = {}
    exec(data.read(), empty)
    return empty['assessment']

def num_of_assessments(k):
    units_dict = get_assess_dict()
    if k in units_dict:
        return len(units_dict[k])
    return 0

def num_of_units():
    units_dict = get_assess_dict()
    num = 0
    for i in units_dict.keys():
        num += 1
    return num

def get_units_list():
    units_dict = get_assess_dict()
    units_list = []
    for i in units_dict.keys():
        units_list.append(units_dict[i])
    return units_list

def get_unit_percentage(num, units_list):
    percentage = 0
    for i in units_list[num]:
        if i['due_string'] != "_multiple _weeks":
            percentage += float(i['weight'])
    return percentage

def get_exam_percentage(num, units_list):
    for i in units_list[num]:
        if i['due_string'] == "Exam Period":
            return i["weight"]
    return 0.00

def add_assessment(course_code, assess):
    data = open("data/data.py", 'r+')
    globs = {}
    exec(data.read(), globs)
    data.close()
    data = open("data/data.py", 'w')
    if course_code in globs['assessment']:
        globs['assessment'][course_code].append(assess)
    else:
        globs['assessment'][course_code] = [assess]
    data.write("assessment = "+str(globs['assessment']))
    data.close()

# This stuff runs when you run this file like `python3 __init__.py` (but not when you import it)
if __name__ == '__main__':
    export('INFO1903')
    while True:
        cusp(input('> '))
