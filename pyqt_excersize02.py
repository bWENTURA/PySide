#!/usr/bin/env python3

import sys
from PySide.QtCore import *
from PySide.QtGui import *

class Form(QDialog):
    def __init__(self, parent = None):
        super(Form, self).__init__(parent)
        self.browser = QTextBrowser()
        self.lineedit = QLineEdit("Type an expression and press Enter")
        self.lineedit.selectAll()
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        layout.addWidget(self.lineedit)
        self.setLayout(layout)
        self.lineedit.setFocus()
        self.connect(self.lineedit, SIGNAL("returnPressed()"), self.updateUi)
        self.setWindowTitle("Calculate")

    def updateUi(self):
        try:
            text = str(self.lineedit.text())
            self.browser.append("%s = <b>%s</b>" % (text, eval(text)))
        except:
            self.browser.append("<font color=red>Text is invalid!</font>")

app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()