import os
from .base import Exporter

class CSVExporter(Exporter):
    def __init__(self, assessments):
        self.lines = []
        super().__init__(assessments)

    def format(self):
        self._add_row(["Assessment Number", "Name", "Due", "Weighting", "Group"])
        for code in self.assessments:
            unit_assessments = self.assessments[code]
            for assessment in unit_assessments:
                self._add_row([
                    code,
                    assessment['assessment_number'],
                    assessment['name'],
                    self._get_due_string(assessment['due_string']),
                    assessment['weight'],
                    assessment['is_group']
                ])

    def export(self, path):
        if not os.path.exists(path): open(path, 'x').close()
        with open(path, 'w') as output_file:
            output_file.write(self._csvify(self.lines))

    def _add_row(self, row):
        self.lines.append(row)

    @staticmethod
    def _csvify(arr):
        return '\n'.join([','.join([str(elem) for elem in row]) for row in arr])
            
    @staticmethod
    def _get_due_string(due_string):
        if due_string == 'Exam Period':
            return 'in the exam period'
        elif due_string == 'Multiple Weeks':
            return 'over multiple weeks'
        else:
            return 'on ' + due_string.lower()
