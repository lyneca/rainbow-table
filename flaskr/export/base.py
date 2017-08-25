class Exporter:
    """
    ABC for Exporter objects
    """
    def __init__(self, assessments):
        self.assessments = assessments
        self.format()

    def export(self, path):
        pass

    def format(self):
        pass
