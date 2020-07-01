'''
Created on 23.06.2020
@author: flori
'''

import sys
import vpython as vp
from PyQt5 import uic, QtCore, QtGui, QtWidgets

class Settings(QtWidgets.QMainWindow):
    def __init__(self, *args, parent = None, **kwargs):
        super(Settings, self).__init__(*args, parent, **kwargs)
        settings = uic.loadUi("settings.ui", self)

class Examples(QtWidgets.QMainWindow):
    def __init__(self, *args, parent = None, **kwargs):
        super(Examples, self).__init__(*args, parent, **kwargs)
        examples = uic.loadUi("examples.ui", self)
        self.actionVerlassen.triggered.connect(self.close)
        self.b_ok.clicked.connect(self.fill)

    def fill(self):
        window.central_mass.setText("123")

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, parent = None, **kwargs):
        super(MainWindow, self).__init__(*args, parent, **kwargs)
        uic.loadUi("entry.ui", self)
        self.b_reset.clicked.connect(self.clear_fields)
        self.actionListe_mit_Voreinstellungen.triggered.connect(self.open_examples)
        self.actionVerlassen.triggered.connect(app.exit)
        self.actionEinstellungen.triggered.connect(self.open_settings)
        self.examples = Examples(parent = self)
        self.settings = Settings(parent = self)

    def clear_fields(self):
        self.central_radius.setText("")
        self.central_mass.setText("")
        self.sat_mass.setText("")
        self.sat_radius.setText("")
        self.distance.setText("")

    def open_examples(self):
        self.examples.show()

    def open_settings(self):
        self.settings.show()

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())
