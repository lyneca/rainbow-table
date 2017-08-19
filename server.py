from bottle import run, post, get, static_file, template, request
import parse

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
    amount_of_units = parse.numOfUnits()
    semester_weeks = 13
    stuff = {}

    # Amount of units:
    stuff["num_units"] = str(amount_of_units)

    # Test (next to Sunday)
    stuff["test"] = ""

    unitsList = parse.getUnitsList()
    unitsDict = parse.getAssessDict()
    string = ''
    for i in unitsDict:
        string += i+","
    stuff["Unit"] = string

    # Units - Assessments Loaded
    string = ""
    for i in range(amount_of_units):
        percent = str(parse.getUnitPercentage(i, unitsList))
        string += percent+","
    stuff["assessments"] = string

    # Units - Exams
    string = ""
    for i in range(amount_of_units):
        percent = str(parse.getExamPercentage(i, unitsList))
        string += percent+","
    stuff["exams"] = string

    # Weeks - Names
    for i in range(semester_weeks):
        stuff["Week"+str(i+1)] = "Meow meow cat!"

    # MIDSEM
    stuff["MIDSEM"] = str("Week off!")

    #Assessment dates being added in?
    for i in range(96):
        stuff["assessment"+str(i+1)] = ''
    days = {'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4, 'Sat': 5, 'Sun': 6}
    assess = parse.getAssessDict()
    for i in assess.keys():
        for j in range(len(assess[i])):
            if assess[i][j]['due_string'] != "Multiple Weeks" and assess[i][j]['due_string'] != "Exam Period":
                due = assess[i][j]['due_string']
                if len(due) < 7:
                    week = int(due[5])-1
                    stuff["assessment"+str(week*7)] = assess[i][j]['name']
                elif due[6] != " ":
                    week = int(due[5]+due[6])
                    if len(due) < 8:
                        stuff["assessment"+str(week*7 -1)] = assess[i][j]['name']
                    else:
                        stuff["assessment"+str(week*7+days[due[9:12]] -1)] = assess[i][j]['name']
                elif due[6] == " ":
                    week = int(due[5])-1
                    stuff["assessment"+str(week*7+days[due[8:11]] +1)] = assess[i][j]['name']



    print(stuff)
    print(type(stuff['num_units']))

    return template(str(TEMPLATE_DIR+'/index.html'), stuff)

@get('/add')
def entry_page():
    return static_file('add.html', root=TEMPLATE_DIR)

@get('/import')
def import_unit():
    return static_file('import.html', root=TEMPLATE_DIR)

@get('/export')
def export_file():
    return static_file('export.html', root=TEMPLATE_DIR)


####################################
# These methods do not serve pages #
####################################

@get('/query')
def query():
    code = request.GET.get("unitCode", None)
    getAssessments(code)

@post('/new')
def new(request):
    "Deal with the POST thing for uploading UOS"


run(debug=True, reload=True)
