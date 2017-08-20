class mdOutput:
    def __init__(self, codes):
        self.courseCodes = codes

    def printToMd(self):
        outputFile = open("templates/output.md", "w")
        outputFile.write("#Assessments\n")
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
                outputFile.write("-Assessment "+str(j['assessment_number'])+ " is "+j['name']+ " and due " +j['due_string']+" (Worth: "+j['weight'] +"%, Group: " + j['is_group']+")\n")
        outputFile.close()




    def getAssignments(self, code):
        ''' For when i thought we were saving as txt files
        f = open("data.txt");
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

a = mdOutput(["INFO1103"])
a.printToMd()
