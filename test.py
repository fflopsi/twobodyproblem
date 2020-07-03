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
        if str(self.choice_central.currentText()) == "Sonne" and str(self.choice_sat.currentText()) == "Erde":
            window.central_mass.setText("1.989e30")
            window.central_radius.setText("6.9634e8")
            window.sat_mass.setText("5.972e24")
            window.sat_radius.setText("6.371e6")
            window.distance.setText("1.496e11")
            self.close()
        elif str(self.choice_central.currentText()) == "Erde" and str(self.choice_sat.currentText()) == "Mond":
            window.central_mass.setText("5.972e24")
            window.central_radius.setText("6.371e6")
            window.sat_mass.setText("7.342e22")
            window.sat_radius.setText("1.737e6")
            window.distance.setText("3.844e8")
            self.close()
        elif str(self.choice_central.currentText()) == "Mond" and str(self.choice_sat.currentText()) == "Sputnik 2":
            window.central_mass.setText("7.342e22")
            window.central_radius.setText("1.737e6")
            window.sat_mass.setText("5e2")
            window.sat_radius.setText("2e0")
            window.distance.setText("1e3")
            self.close()
        elif str(self.choice_central.currentText()) == "Erde" and str(self.choice_sat.currentText()) == "Sputnik 2":
            window.central_mass.setText("5.972e24")
            window.central_radius.setText("6.371e6")
            window.sat_mass.setText("5e2")
            window.sat_radius.setText("2e0")
            window.distance.setText("1e3")
            self.close()
        elif str(self.choice_central.currentText()) == "Sonne" and str(self.choice_sat.currentText()) == "Mond":
            window.central_mass.setText("1.989e30")
            window.central_radius.setText("6.9634e8")
            window.sat_mass.setText("7.342e22")
            window.sat_radius.setText("1.737e6")
            window.distance.setText("1.496e11")
            self.close()
        elif str(self.choice_central.currentText()) == "Sonne" and str(self.choice_sat.currentText()) == "Sputnik 2":
            window.central_mass.setText("1.989e30")
            window.central_radius.setText("6.9634e8")
            window.sat_mass.setText("5e2")
            window.sat_radius.setText("2e0")
            window.distance.setText("1.496e11")
            self.close()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("falsche Wahl")
            msg.setWindowTitle("Fehler")
            msg.exec()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, parent = None, **kwargs):
        super(MainWindow, self).__init__(*args, parent, **kwargs)
        uic.loadUi("entry.ui", self)
        self.examples = Examples(parent = self)
        self.settings = Settings(parent = self)
        self.b_reset.clicked.connect(self.clear_fields)
        self.actionListe_mit_Voreinstellungen.triggered.connect(self.examples.show)
        self.actionVerlassen.triggered.connect(app.exit)
        self.actionEinstellungen.triggered.connect(self.settings.show)

    def clear_fields(self):
        self.central_radius.setText("")
        self.central_mass.setText("")
        self.sat_mass.setText("")
        self.sat_radius.setText("")
        self.distance.setText("")

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())
