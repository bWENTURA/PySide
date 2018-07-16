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

class View(QDialog):
    def __init__(self, parent = None):
        super(View, self).__init__(parent)
        self.setGeometry(300, 100, const.dialogWidth, const.dialogHeight)
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        self.set_number()
        self.count_set()
        self.setWindowTitle("Cows and Bulls")
        self.presentProgressList = QListWidget()
        self.presentProgressList.setMinimumWidth(const.presentProgressListWidth)
        self.ProgressList = QListWidget()
        self.nextButton = QPushButton("New game")
        self.nextButton.setFixedWidth(150)
        self.nextButton.setStyleSheet("background-color: None")
        self.quitButton = QPushButton("Quit game")
        self.quitButton.setFixedWidth(150)
        self.quitButton.setStyleSheet("background-color: None")
        self.showButton = QPushButton("Show number")
        self.showButton.setFixedWidth(150)
        self.showButton.setStyleSheet("background-color: None")
        self.lineInput = QLineEdit("Enter here.")
        self.lineInputLabel = QLabel("Enter number from range [1000, 9999] here and accept it by hiting 'enter:")
        self.organizeWidget()

    def organizeWidget(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Current session Progresss:"))
        layout.addWidget(self.presentProgressList)
        tempWidgetPresentInput = QWidget()
        tempWidgetPresentInput.setLayout(layout)

        layout = QGridLayout()
        layout.addWidget(QLabel("Menu:"), 0, 0)
        layout.addWidget(self.nextButton, 1, 0)
        layout.addWidget(self.showButton, 1, 1)
        layout.addWidget(self.quitButton, 2, 0)
        tempWidgetMenu = QWidget()
        tempWidgetMenu.setLayout(layout)

        layout = QVBoxLayout()
        layout.addWidget(tempWidgetMenu)
        layout.addWidget(QLabel("Progress:"))
        layout.addWidget(self.ProgressList)
        tempWidgetMenuResult = QWidget()
        tempWidgetMenuResult.setLayout(layout)

        layout = QHBoxLayout()
        layout.addWidget(tempWidgetPresentInput)
        layout.addWidget(tempWidgetMenuResult)
        tempWidget = QWidget()
        tempWidget.setLayout(layout)

        layout = QVBoxLayout()
        layout.addWidget(tempWidget)
        layout.addWidget(self.lineInputLabel)
        layout.addWidget(self.lineInput)

        self.setLayout(layout)
        # self.clicked.connect = self.updateKeyEvent
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
    
    def updateUi(self):
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
            self.presentProgressList.scrollToBottom()
        except BadLenght:
            self.presentProgressList.addItem("You didn't entered number from range [0, 9999] using 4-digits.")
            self.presentProgressList.scrollToBottom()
        except BadSign:
            self.presentProgressList.addItem("There is unappropriate sign in your input.") #example -000
            self.presentProgressList.scrollToBottom()
        except:
            self.presentProgressList.addItem("You haven't entered number correctly.")
            self.presentProgressList.scrollToBottom()
        else:
            if guess_number == self.number:
                self.count += 1
                self.presentProgressList.clear()
                self.presentProgressList.addItem("You guessed well the number {}!\nClick 'New game' to play again or 'Quit game' to end game."
                .format("".join(self.number)))
                self.presentProgressList.scrollToBottom()
                self.ProgressList.addItem("{} guessed after {} attempts.".format("".join(self.number), self.count))
                self.ProgressList.scrollToBottom()
                self.count_set()
                self.lineInput.clear()
                self.lineInput.setReadOnly(True)
                self.lineInput.returnPressed.disconnect(self.updateUi)
            else:
                self.presentProgressList.addItem("You've got {} cows and {} bulls with {}."
                .format(*count_cows_and_bulls(self.number, guess_number), "".join(guess_number)))
                self.presentProgressList.scrollToBottom()
                self.count += 1
        self.lineInput.setFocus()
        self.lineInput.selectAll()

    def updateKeyEvent(self):
        pass

    def updateNextButton(self):
        self.set_number()
        self.count_set()
        self.presentProgressList.clear()
        self.presentProgressList.addItem("New number has been drawn.")
        self.presentProgressList.scrollToBottom()
        self.lineInput.clear()
        self.lineInput.insert("Try guess new number.")
        self.lineInput.setFocus()
        self.lineInput.selectAll()
        if self.lineInput.isReadOnly():
            self.lineInput.setReadOnly(False)
            self.connect(self.lineInput, SIGNAL("returnPressed()"), self.updateUi)

    def updateQuitButton(self):
        self.close()

    def updateShowButton(self):
        if not self.lineInput.isReadOnly():
            self.presentProgressList.clear()
            self.presentProgressList.addItem("The number is {},\nclick 'New game' to enter new session or 'Quit game' to exit program."
            .format("".join(self.number)))
            self.presentProgressList.scrollToBottom()
            self.ProgressList.addItem("{} no successful guess.".format("".join(self.number)))
            self.ProgressList.scrollToBottom()
            self.lineInput.clear()
            self.lineInput.setReadOnly(True)
            self.lineInput.returnPressed.disconnect(self.updateUi)

    def set_number(self):
        self.number = list(str(random.choice(range(0, 10000))).zfill(4))
        

    def count_set(self):
        self.count = 0

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = View()
    view.show()
    app.exec_()