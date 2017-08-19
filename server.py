from bottle import run, post, get, static_file, template, request
import re
import parse

class Ass:
    def __init__(self, code, name, week):
        self.code = code
        self.name = name
        self.week = week
        self.color = hex(hash(self.code))[2:8]

    def __str__(self):
        return self.code + ' ' + self.name

def get_week(s):
    finds = re.match(r'[Ww]eek ?(\d+)', s)
    if not finds:
        return None 
    return int(finds.groups()[0])

def getAssessments(course_code):
    parse.export(course_code)

TEMPLATE_DIR = './templates'


"""
Endpoints:
    GET  /               index()      - Serves the main page. View and query timetables, with an export button.
    GET  /manual         entry_page() - Serves the page for manually entering data.
    GET  /query?c=[code] query()      - Queries the database for assessments.
    POST /new            new_entry()  - Enter a new entry to the database.
"""

@get('/global.css')
def css():
    return static_file('global.css', root=TEMPLATE_DIR)

@get('/')
def index():
    data = {'weeks': [x for x in range(17)], 'ass': []}

    data['num_units'] = 7
    data['weeks'][8] = "Midterm Break"
    data['weeks'][14] = "STUVAC"
    data['weeks'][15] = "Exam Week"
    data['weeks'][16] = "Exam Week"

    flag = 0
    for i in range(17):
        if type(data['weeks'][i]) is not int:
            flag = 1
            continue
        data['weeks'][i] = "Week %s" % (i + 1 - flag)

    # Assessment dates being added in?
    assess = parse.getAssessDict()
    for code in assess:
        for ass in assess[code]:
            if ass['due_string'] != "Multiple Weeks":
                if i in data['weeks']:
                    i += 1
                w = get_week(ass['due_string'])
                if not w: continue
                data['ass'].append(Ass(code, ass['name'], w))
    return template(str(TEMPLATE_DIR+'/index_.html'), data)

@get('/add')
def entry_page():
    return static_file('add.html', root=TEMPLATE_DIR)

@get('/import')
def import_unit():
    return static_file('import.html', root=TEMPLATE_DIR)



####################################
# These methods do not serve pages #
####################################

@get('/query')
def query():
    code = request.GET.get("unitCode", None)
    getAssessments(code)

@post('/new')
def new():
    "Deal with the POST thing for uploading UOS"


run(debug=True, reload=True)
