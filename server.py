from bottle import run, post, get, static_file, template
#import parser

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
    amount_of_units = 5
    semester_weeks = 13
    stuff = {}

    # Test (next to Sunday)    
    stuff["test"] = ""

    # Units - Assessments Loaded
    for i in range(amount_of_units):
        stuff["loaded_u"+str(i+1)] = str(20+10*i)

    # Units - Exams
    for i in range(amount_of_units):
        stuff["exam_u"+str(i+1)] = str(20+10*i)

    # Weeks - Names
    for i in range(semester_weeks):
        stuff["Week"+str(i+1)] = "Meow meow cat!"

    # MIDSEM
    stuff["MIDSEM"] = str("Week off!")

    print(stuff)

    return template(str(TEMPLATE_DIR+'/index.html'), stuff)

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
    "Query result or whatever lol"

@post('/new')
def new():
    # somehow get post response
    "some okay response"


run(reload=True)
