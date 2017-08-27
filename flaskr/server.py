from flask import Flask, render_template, request
import os
import re
import parse
import random
import export.md as md
import export.csv as csv
import export.pdf as pdf 

TEMPLATE_DIR = './templates'
EXPORT_DIR = './export'


template_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(template_dir, 'templates')
print(template_dir)

app = Flask(__name__, template_folder=template_dir)

"""
@app.route('/')
def display():
    return "Looks like it works!"
"""

def pad(s, n):
    return '0'*(n-len(s))+s

def lighten(x):
    x = eval('0x' + x)
    if 200 > x or x < 120:
        x = random.randrange(120, 200)
    return hex(x)[2:]

def twos(x):
    return (x[:2],x[2:4],x[4:])


class Ass:
    def __init__(self, code, name, week, weight):
        self.code = code
        self.name = name
        self.week = week
        self.weight = weight.split('.')[0]
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

def get_assessments(course_code):
    parse.export(course_code)



"""
Endpoints:
    GET  /               index()      - Serves the main page. View and query timetables, with an export button.
    GET  /manual         entry_page() - Serves the page for manually entering data.
    GET  /query?c=[code] query()      - Queries the database for assessments.
    POST /new            new_entry()  - Enter a new entry to the database.
"""

@app.route('/global.css')
def css():
    return static_file('global.css', root=TEMPLATE_DIR)

# Home page
@app.route('/')
def index():
    data = {'weeks': [x for x in range(17)], 'ass': []}

    data['num_units'] = parse.num_of_units()
    data['weeks'][8] = "Midterm Break"
    data['weeks'][14] = "STUVAC"
    data['weeks'][15] = "Exam Week"
    data['weeks'][16] = "Exam Week"
    data['pad'] = pad
    flag = 0
    for i in range(17):
        if type(data['weeks'][i]) is not int:
            flag = 1
            continue
        data['weeks'][i] = "Week %s" % (i + 1 - flag)

    # Assessment dates being added in?
    amount_of_units = parse.num_of_units()
    units_list = parse.get_units_list()
    units_dict = parse.get_assess_dict()
    data["unit_loaded"] = []
    for i in units_dict:
        data["unit_loaded"].append("%s"%i)

    # Units - Assessments Loaded
    data["unit_assess"] = []
    for i in range(amount_of_units):
        percent = str(parse.get_unit_percentage(i, units_list))
        data["unit_assess"].append("%s" % percent)

    # Units - Exams
    data["unit_exam"] = []
    for i in range(amount_of_units):
        percent = str(parse.get_exam_percentage(i, units_list))
        data["unit_exam"].append("%s" % percent)

    # Assessment dates being added in?
    assess = parse.get_assess_dict()
    data["multiple_name"] = []
    data["multiple_weight"] = []
    data["multiple_counted"] = []
    for code in assess:
        multi_name = []
        multi_weight = []
        multi_count = 0
        for ass in assess[code]:
            if ass['due_string'] != "Multiple Weeks":
                if i in data['weeks']:
                    i += 1
                w = get_week(ass['due_string'])
                if not w: continue
                data['ass'].append(Ass(code, ass['name'], w, ass['weight']))
            else:
                if ass['name']:
                    multi_name.append("%s" % ass['name'])
                    multi_weight.append("%s" % ass['weight'])
                    multi_count += 1
        print(multi_name)
        print(multi_weight)
        print(multi_count)
        data["multiple_counted"].append(multi_count)
        data["multiple_name"].append(multi_name)
        data["multiple_weight"].append(multi_weight)






    return render_template(str('/index.html'), data=data)

# Add Assessment
@app.route('/add')
def entry_page():
    return static_file('add.html', root=TEMPLATE_DIR)

# Import Unit
@app.route('/import')
def import_unit():
    return static_file('import.html', root=TEMPLATE_DIR)

@app.route('/export')
def export():
    return static_file('export.html', root=TEMPLATE_DIR)

# Export Planner
@app.route('/export/csv')
def export_csv():
    exporter = csv.CSVExporter(parse.get_assess_dict())
    exporter.export('export/output.csv')
    return static_file('output.csv', root=EXPORT_DIR)


@app.route('/export/md')
def export_md():
    exporter = md.MDExporter(parse.get_assess_dict())
    exporter.export('export/output.md')
    return static_file('output.md', root=EXPORT_DIR)

@app.route('/export/pdf')
def export_pdf():
    exporter = pdf.PDFExporter(parse.get_assess_dict())
    exporter.export('export/output.pdf')
    return static_file('output.pdf', root=EXPORT_DIR)

# Is not linked currently!
# DO NOT MAKE LINKED!!!
# NOT TESTED!!!!!!
@app.route('/online')
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
    return render_template(str(TEMPLATE_DIR+'/index.html'), data)


####################################
# These methods do not serve pages #
####################################

@app.route('/query')
def query():
    code = request.GET.get("unitCode", None)
    get_assessments(code)
    redirect("/")


@app.route('/new')
def new():
    code = request.forms.get("unitCode")
    name = request.forms.get("assName")
    weight = request.forms.get("assessWeight")
    date_due = request.forms.get("dateDue")
    time_due = request.forms.get("timeDue")
    assess_num = parse.num_of_assessments(code)
    parse.add_assessment(code, {'assessment_number': assess_num, 'name': name, 'is_group': "_no", 'weight': weight, 'due_string': date_due[:-1]+" "+time_due})
    redirect("/")


app.run(debug=True, port=8008)