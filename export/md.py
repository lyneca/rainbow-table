import os

class MDExporter(Exporter):
    def __init__(self, assessments):
        super().__init__(self, assessments)
        self.lines = []

    def format(self):
        self._add_header('Semester Assessment Timetable')
        if not os.path.exists("output.csv"): open("output.csv", 'x').close()
        for code in self.assessments:
            self._add_header(code, 2)
            table = [['#', 'Name', 'Weight', 'Due', 'Group']]
            for assessment in self.assessments[code]:
                table.append([
                    assessment['assessment_number'],
                    assessment['name'],
                    assessment['weight'],
                    assessment['due_string'],
                    assessment['is_group']
                ])
                self._add_table(table)

    def export(self):
        with open("output.md", 'x') as output_file:
            output_file.write('\n'.join(self._lines))

    def _add_header(self, text, level=1):
        self._add_line('#' * level + ' ' + text)

    def _add_table(self, table):
        if not table: return
        self._add_line('| ' + ' | '.join([str(x) for x in table[0]]))
        self._add_line(' | '.join(['---'] * len(table[0])))
        for line in table[1:]:
            self._add_line(' | '.join([str(x) for x in line]))

    def _add_line(self, string):
        self.lines.append(string)
