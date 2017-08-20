from bottle import run, post, get, static_file, template, request, redirect
import re
import parse
import random
import mdOutput as md
import csvOutput as csv

def lighten(x):
    x = eval('0x' + x)
    if 200 > x or x < 120:
        x = random.randrange(120, 200)
    return hex(x)[2:]

def twos(x):
    return (x[:2],x[2:4],x[4:])


class Ass:
    def __init__(self, code, name, week):
        self.code = code
        self.name = name
        self.week = week
        self.color = hex(abs(hash(self.code)))[2:8]
        random.seed(self.color)
        self.color = ''.join([lighten(x) for x in twos(self.color)])

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

# Home page
@get('/')
def index():
    data = {'weeks': [x for x in range(17)], 'ass': []}

    data['num_units'] = parse.numOfUnits()
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
    amount_of_units = parse.numOfUnits()
    unitsList = parse.getUnitsList()
    unitsDict = parse.getAssessDict()
    string = ''
    for i in unitsDict:
        string += i+","
    data["Unit"] = string

    # Units - Assessments Loaded
    string = ""
    for i in range(amount_of_units):
        percent = str(parse.getUnitPercentage(i, unitsList))
        string += "%s," % percent
    data["Asses"] = string

    # Units - Exams
    string = ""
    for i in range(amount_of_units):
        percent = str(parse.getExamPercentage(i, unitsList))
        string += "%s," % percent
    data["Exam"] = string

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
    print(data)
    return template(str(TEMPLATE_DIR+'/index.html'), data)

# Add Assessment
@get('/add')
def entry_page():
    return static_file('add.html', root=TEMPLATE_DIR)

# Import Unit
@get('/import')
def import_unit():
    return static_file('import.html', root=TEMPLATE_DIR)

# Export Planner
@get('/export')
def import_unit():
    codes = parse.getAssessDict() # List of unit codes
    csvFormat = csv.csvOutput(codes)
    csvFormat.printToCsv()
    mdFormat = md.mdOutput(codes)
    mdFormat.printToMd()
    return static_file('export.html', root=TEMPLATE_DIR)

# Is not linked currently!
# DO NOT MAKE LINKED!!!
# NOT TESTED!!!!!!
@post('/online')
def online():
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
    return template(str(TEMPLATE_DIR+'/index.html'), data)


####################################
# These methods do not serve pages #
####################################

@get('/query')
def query():
    code = request.GET.get("unitCode", None)
    getAssessments(code)
    redirect("/")


@post('/new')
def new():
    code = request.forms.get("unitCode")
    name = request.forms.get("assName")
    weight = request.forms.get("assessWeight")
    date_due = request.forms.get("dateDue")
    time_due = request.forms.get("timeDue")
    assess_num = parse.numOfAssessments(code)
    parse.addAssessment(code, {'assessment_number': assess_num, 'name': name, 'is_group': "No", 'weight': weight, 'due_string': date_due[:-1]+" "+time_due})
    redirect("/")


run(debug=True, reload=True)
