from bottle import route, run, post, get, debug, template, request, response, static_file, error

@route('/', method="GET")
@get('/')
def index():
    static_file("notifyMe.js", root=".")
    return """<h1>This is an amazing webpage!</h1>
<p>No don't leave!!!</p>
<p>Have a look at <a href="/tables">this!</a></p>
<p>Press here to run test the template: </p>
<form action="/test_template" method="post">
    <input value="TEST!" type="submit"/></form>"""

@route('/tables', method="GET")
@get('/tables')
def showTables():
    return template('index.html')

@route('/test_template', method="POST")
@post('/test_template')
def testTemplate():
    return template('test_template.html', "")

@route('/editStatus', method="GET")
@get('/editStatus')
def editTemplate():
    status = request.GET.status.strip()
    if status == 'open':
        status = 1
        return "You requested OPEN!"
    else:
        status = 0
        return ""

@route('/edit', method="GET")
@get('/edit')
def forceEdit():
    mistake404()

@error(403)
def mistake403(code):
    return 'There is a mistake in your url!'


@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'

debug(True)
run(reloader=True)
# remember to remove reloader=True and debug(True) when you move your
# application from development to a productive environment