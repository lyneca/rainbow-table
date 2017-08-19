import requests
from pprint import pprint
from bs4 import BeautifulSoup

def parse(course_code):
    pass

def get_page(link):
    r = requests.get(link)
    r.raise_for_status()
    return r.content

def cusp(course_code):
    html = get_page('https://cusp.sydney.edu.au/students/view-unit-page/alpha/' + course_code)
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find(string="Assessment Methods:").parent.next_element.next_element.next_element.next_element.next_element
    list_ds = [[x.text.strip() for x in x.find_all('td')][:-1] for x in table.find_all('tr')][1:]
    dict_ds = [{
        'assessment_number': x[0],
        'name': x[1],
        'is_group': x[2],
        'weight': x[3],
        'due_string': x[4]
    } for x in list_ds]
    return dict_ds 

if __name__ == '__main__':
    pprint(cusp('INFO1103'))
