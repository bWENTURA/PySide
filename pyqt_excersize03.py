#!/usr/bin/env python3

import sys
import urllib
from PySide.QtCore import *
from PySide.QtGui import *

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.rates = {"USD" : 15, "PLN" : 10, "LPG" : 2}
        self.fromComboBox = QComboBox()
        self.fromComboBox.addItems(list(self.rates.keys()))
        self.fromSpinBox = QDoubleSpinBox()
        self.fromSpinBox.setRange(0.01, 10000000.00)
        self.fromSpinBox.setValue(1.00)
        self.toComboBox = QComboBox()
        self.toComboBox.addItems(list(self.rates.keys()))
        self.toLabel = QLabel("1.00")

        grid = QGridLayout()
        grid.addWidget(self.fromComboBox, 0, 0)
        grid.addWidget(self.fromSpinBox, 0, 1)
        grid.addWidget(self.toComboBox, 1, 0)
        grid.addWidget(self.toLabel, 1, 1)
        self.setLayout(grid)

        self.connect(self.fromComboBox, SIGNAL("currentIndexChanged(int)"), self.updateUi)
        self.connect(self.toComboBox, SIGNAL("currentIndexChanged(int)"), self.updateUi)
        self.connect(self.fromSpinBox, SIGNAL("valueChanged(double)"), self.updateUi)
        self.setWindowTitle("Currency")

    def updateUi(self):
        to = self.toComboBox.currentText()
        from_ = self.fromComboBox.currentText()
        amount = (self.rates[from_] / self.rates[to])*self.fromSpinBox.value()
        self.toLabel.setText("%0.2f" % amount)

app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()