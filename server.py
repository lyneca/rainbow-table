from bottle import run, post, get, static_file

"""
Endpoints:
    GET  /               index()      - Serves the main page. View and query timetables, with an export button.
    GET  /manual         entry_page() - Serves the page for manually entering data.
    GET  /query?c=[code] query()      - Queries the database for assessments.
    POST /new            new_entry()  - Enter a new entry to the database.
"""

def get_html(p):
    return open(p + '.html').read()

def get_css(p):
    return open(p + '.css').read()

@get('/global.css')
def css():
    return static_file('global.css', root='.')

@get('/')
def index():
    return static_file('index.html', root='.')

@get('/add')
def entry_page():
    return static_file('add.html', root='.')

@get('/import')
def import_unit():
    return static_file('import.html', root='.')



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
