import os
from markdown2 import markdown
from .md import Exporter, MDExporter
import pdfkit

class PDFExporter(Exporter):
    def __init__(self, assessments):
        super().__init__(assessments)

    def format(self):
        self.md = MDExporter(self.assessments).as_text()
        self.html = markdown(self.md, extras=["tables"])
        self.pdf = pdfkit.from_string(self.html, False, css='templates/github.css')

    def export(self, path):
        if not os.path.exists(path): open(path, 'x').close()
        with open(path, 'wb') as output_file:
            output_file.write(self.pdf)
