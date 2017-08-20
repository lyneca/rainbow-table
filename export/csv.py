class CSVExporter:
    def __init__(self, assessments):
        self.lines = []
        self.add_row(["Assessment Number", "Name", "Due", "Weighting", "Group"])
        for code in assessments:
            assessment = assessments[code]
            self.add_row([
                assessment['assessment_number'],
                assessment['name'],
                self.get_due_string(assessment['due_string'])
                assessment['weight'],
                assessment['is_group']
            ])

    def export(self):
        if not os.path.exists("output.csv"): open("output.csv", 'x').close()
        with open("output.csv") as output_file:
            output_file.write(self.csvify(array))

    def add_row(self, row):
        self.lines.append(row)

    @staticmethod
    def csvify(arr):
        return '\n'.join([','.join([str(elem) for elem in row]) for row in lines])
            
    @staticmethod
    def get_due_string(string):
        if due_string == 'Exam Period':
            return 'in the Exam Period'
        elif due_string == 'Multiple Weeks':
            return 'over multiple weeks'
        else:
            return 'on ' + due_string
