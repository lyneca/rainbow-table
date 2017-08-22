import os
from .base import Exporter

class MDExporter(Exporter):
    def __init__(self, assessments):
        self.lines = []
        super().__init__(assessments)

    def format(self):
        self._add_header('Semester Assessment Timetable')
        if not os.path.exists("output.md"): open("output.md", 'x').close()
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

    def as_text(self):
        return '\n'.join(self.lines)

    def export(self, path):
        if not os.path.exists(path): open(path, 'x').close()
        with open(path, 'w') as output_file:
            output_file.write('\n'.join(self.lines))

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
