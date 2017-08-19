import csv
class csvOutput:
    def __init__(self, codes):
        self.courseCodes = codes

    def printToCsv(self):
        outputFile = open("/templates/output.csv", "w")
        writer = csv.writer(outputFile)
        writer.writerow(["Assessment Number", "Name", "Due", "Weighting", "Group"])
        for i in self.courseCodes:
            assignments = self.getAssignments(i)
            if assignments == None:
                return None
            for j in assignments:
                if j['due_string'] == 'Exam Period':
                    j['due_string'] = 'in the Exam Period'
                elif j['due_string'] == 'Multiple Weeks':
                    j['due_string'] = 'over multiple weeks'
                else:
                    j['due_string'] = 'on '+j['due_string']
                writer.writerow([str(j['assessment_number']), j['name'], j['due_string'], j['weight'], j['is_group']])
        outputFile.close()




    def getAssignments(self, code):
        '''f = open("data.txt");
        text = f.read()
        f.close()
        o = open("example.py", "w")
        o.write("assessment = "+text)
        o.close()'''
        from data import data
        data = data.assessment
        if code not in data:
            return None
        return data[code]
