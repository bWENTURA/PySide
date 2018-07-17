#!/usr/bin/env python3

import sys
import random
from PySide.QtCore import *
from PySide.QtGui import *

class const():
    dialogWidth = 1000
    dialogHeight = 500
    presentProgressListWidth = 0.6 * dialogWidth
    progressListWidth = dialogWidth - presentProgressListWidth
    pushButtonSize = 150

class NoInput(Exception):
    pass

class BadLenght(Exception):
    pass

class BadSign(Exception):
    pass

def count_cows_and_bulls(number, guess_number):
    cows, bulls, table, guess_table = 0, 0, [], []
    for i in range(4):
        if guess_number[i] == number[i]:
            cows += 1
        else:
            table.append(number[i])
            guess_table.append(guess_number[i])
    for i in range(len(table)):
        if guess_table[i] in table:
            table.remove(guess_table[i])
            bulls += 1
    return [cows, bulls]

class View(QWidget):
    def __init__(self, parent = None):
        super(View, self).__init__(parent)
        self.setGeometry(300, 100, const.dialogWidth, const.dialogHeight)
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint & ~Qt.WindowMinimizeButtonHint & ~Qt.WindowMaximizeButtonHint)
        self.setWindowTitle("Cows and Bulls")
        
        self.showAdditional = True
        self.set_number()
        self.count_set()

        self.presentProgressList = QListWidget()
        self.presentProgressList.setMinimumWidth(const.presentProgressListWidth)
        self.ProgressList = QListWidget()

        self.nextButton = QPushButton("New game")
        self.nextButton.setFixedWidth(const.pushButtonSize)
        self.nextButton.setStyleSheet("background-color: None")

        self.quitButton = QPushButton("Quit game")
        self.quitButton.setFixedWidth(const.pushButtonSize)
        self.quitButton.setStyleSheet("background-color: None")

        self.showButton = QPushButton("Show number")
        self.showButton.setFixedWidth(const.pushButtonSize)
        self.showButton.setStyleSheet("background-color: None")

        self.lineInput = QLineEdit("Enter here.")
        self.organizeWidget()

    def organizeWidget(self):
        '''
            Function organize the look of widget.
        '''
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Current session progress:"))
        layout.addWidget(self.presentProgressList)
        layout.addWidget(QLabel("Enter number from range [0, 9999] here and accept it by hitting 'enter':"))
        layout.addWidget(self.lineInput)
        tempWidgetPresentProgressInput = QWidget()
        tempWidgetPresentProgressInput.setLayout(layout)

        layout = QGridLayout()
        layout.addWidget(QLabel("Menu:"), 0, 0)
        layout.addWidget(self.nextButton, 1, 0)
        layout.addWidget(self.showButton, 1, 1)
        layout.addWidget(self.quitButton, 2, 0)
        tempWidgetMenu = QWidget()
        tempWidgetMenu.setLayout(layout)

        layout = QVBoxLayout()
        layout.addWidget(tempWidgetMenu, 0, Qt.AlignLeft)
        layout.addWidget(QLabel("Progress:"))
        layout.addWidget(self.ProgressList)
        tempWidgetMenuResult = QWidget()
        tempWidgetMenuResult.setLayout(layout)

        layout = QHBoxLayout()
        layout.addWidget(tempWidgetPresentProgressInput)
        layout.addWidget(tempWidgetMenuResult)
        tempWidget = QWidget()
        tempWidget.setLayout(layout)

        self.setLayout(layout)
        '''
            Series of instructions to organize focus and key events of Dialog window.
        '''
        self.keyPressEvent = self.updateDialogKeyPolicy
        self.nextButton.clicked.connect(self.updateNextButton)
        self.showButton.clicked.connect(self.updateShowButton)
        self.quitButton.clicked.connect(self.updateQuitButton)
        self.lineInput.returnPressed.connect(self.updateUi)

        self.nextButton.setFocusPolicy(Qt.NoFocus)
        self.showButton.setFocusPolicy(Qt.NoFocus)
        self.quitButton.setFocusPolicy(Qt.NoFocus)
        self.presentProgressList.setFocusPolicy(Qt.NoFocus)
        self.ProgressList.setFocusPolicy(Qt.NoFocus)

        self.lineInput.setFocus()
        self.lineInput.selectAll()

    def updateDialogKeyPolicy(self, event):
        pass
    
    def updateUi(self):
        self.showAdditional = True
        try:
            text = str(self.lineInput.text())
            if not text:
                raise NoInput
            guess_number = list(text.zfill(4))
            if len(guess_number) != 4:
                raise BadLenght
            for digit in guess_number:
                if not digit.isnumeric():
                    raise BadSign
        except NoInput:
            self.presentProgressList.addItem("You entered empty input.")
        except BadLenght:
            self.presentProgressList.addItem("You didn't entered number from range [0, 9999] using 4-digits.")
        except BadSign:
            self.presentProgressList.addItem("There is unappropriate sign in your input.") #example -000
        except:
            self.presentProgressList.addItem("You haven't entered number correctly.")
        else:
            if guess_number == self.number:
                self.count += 1
                self.presentProgressList.clear()
                self.presentProgressList.addItem("You guessed well the number {}!\nClick 'New game' to play again or 'Quit game' to end game."
                .format("".join(self.number)))
                self.ProgressList.addItem("{} guessed after {} attempts.".format("".join(self.number), self.count))
                self.ProgressList.scrollToBottom()
                self.count_set()
                self.lineInput.clear()
                self.lineInput.setReadOnly(True)
                self.lineInput.returnPressed.disconnect(self.updateUi)
                self.showAdditional = False
            else:
                self.presentProgressList.addItem("You've got {} cows and {} bulls with {}."
                .format(*count_cows_and_bulls(self.number, guess_number), "".join(guess_number)))
                self.count += 1
        self.presentProgressList.scrollToBottom()
        self.lineInput.setFocus()
        self.lineInput.selectAll()

    def updateNextButton(self):
        '''
            New slot(?) for signal 'clicked' when 'New game' button is clicked.
        '''
        self.presentProgressList.clear()
        if self.showAdditional:
            self.presentProgressList.addItem("The number was: {}".format("".join(self.number)))
            self.ProgressList.addItem("{} no successful guess.".format("".join(self.number)))
        else:
            self.showAdditional = True
        self.set_number()
        self.count_set()
        self.presentProgressList.addItem("New number has been drawn.")
        self.lineInput.insert("Try guess new number.")
        self.lineInput.setFocus()
        self.lineInput.selectAll()
        if self.lineInput.isReadOnly():
            self.lineInput.setReadOnly(False)
            self.lineInput.returnPressed.connect(self.updateUi)
        

    def updateQuitButton(self):
        '''
            New slot for signal 'clicked' for 'Quit button'.
        '''
        self.close()

    def updateShowButton(self):
        '''
            New slot for signal 'clicked' for 'Show number'.
        '''
        if not self.lineInput.isReadOnly():
            self.presentProgressList.clear()
            self.presentProgressList.addItem("The number was {},\nclick 'New game' to enter new session or 'Quit game' to exit program."
            .format("".join(self.number)))
            self.presentProgressList.scrollToBottom()
            self.ProgressList.addItem("{} no successful guess.".format("".join(self.number)))
            self.ProgressList.scrollToBottom()
            self.lineInput.clear()
            self.lineInput.setReadOnly(True)
            self.lineInput.returnPressed.disconnect(self.updateUi)
            self.showAdditional = False

    def set_number(self):
        '''
            Function which sets new value of number to be guessed.
        '''
        self.number = list(str(random.choice(range(0, 10000))).zfill(4))
        

    def count_set(self):
        '''
            Function which attempts counter to 0.
        '''
        self.count = 0

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = View()
    view.show()
    app.exec_()