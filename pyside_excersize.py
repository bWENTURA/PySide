#!/usr/bin/env python3


import sys
from PySide.QtGui import *
from PySide.QtCore import *

# Create the application object

app = QApplication(sys.argv)


# Create a simple dialog box

msg_box = QMessageBox()

msg_box.setText("Hello World!")

msg_box.show()


sys.exit(msg_box.exec_())