from bottle import run, post, get

"""
Endpoints:
    GET  /               index()      - Serves the main page. View and query timetables, with an export button.
    GET  /manual         entry_page() - Serves the page for manually entering data.
    GET  /query?c=[code] query()      - Queries the database for assessments.
    POST /new            new_entry()  - Enter a new entry to the database.
"""

@get('/')
def index():
    return "<p>Hello, world!</p>"  # should actually return the index page lol

@get('/manual')
def entry_page():
    return "Entry page"

@get('/query')
def query():
    return "Query result or whatever lol"

@post('/new')
def new():
    # somehow get post response
    return "some okay response"
