class MDExporter:
    def __init__(self, assessments):
        self.assessments = assessments
        self.lines = []

    def export(self):
        self.add_header('Semester Assessment Timetable')
        if not os.path.exists("output.csv"): open("output.csv", 'x').close()
        for code in self.assessment:
            add_header(code, 2)
            table = [['#', 'Name', 'Weight', 'Due', 'Group']]
            for assessment in assessments[code]:
                table.append([
                    assessment['assessment_number'],
                    assessment['name'],
                    assessment['weight'],
                    assessment['due_string'],
                    assessment['is_group']
                ])
        with open("output.csv") as output_file:
            output_file.write('\n'.join(self.lines))

    def add_header(self, text, level=1):
        self.add_line('#' * level + ' ' + text)

    def add_line(self, string):
        self.lines.append(string)

a = mdOutput(["INFO1103"])
a.printToMd()
