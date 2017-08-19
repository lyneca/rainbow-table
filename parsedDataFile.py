import json

class parsedDataFile:
    name = ""
    jsonAssess = ""
    assess = ""
    #Gets string of UOS name and assessments JSON
    def __init__(self, uosName, assessments):
        self.name = uosName
        self.jsonAssess = assessments
        self.assess = json.loads(assessments)

    #Saves assessments in file named after the unit of study
    def saveAsFile(self):
        f = open("Subjects/"+self.name, 'w')
        f.write(self.name+", "+self.jsonAssess+"\n")
        f.close()
