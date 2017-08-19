from bottle import run, post, get, static_file

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
    return static_file('index.html', root=TEMPLATE_DIR)

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
    return "Query result or whatever lol"

@post('/new')
def new():
    # somehow get post response
    return "some okay response"


run(reload=True)
