'''
Created on 23.06.2020
@author: flori
'''

import sys, data
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
        self.b_ok.clicked.connect(self.ok)
        self.b_fill.clicked.connect(self.fill)

    def fill(self):
        if data.MASS[str(self.choice_central.currentText())] <= data.MASS[str(self.choice_sat.currentText())]:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Wahl nicht möglich")
            msg.setWindowTitle("Fehler")
            msg.exec()
        else:
            window.central_mass.setText(str(data.MASS[str(self.choice_central.currentText())]))
            window.central_radius.setText(str(data.RADIUS[str(self.choice_central.currentText())]))
            window.sat_mass.setText(str(data.MASS[str(self.choice_sat.currentText())]))
            window.sat_radius.setText(str(data.RADIUS[str(self.choice_sat.currentText())]))
            window.distance.setText(str(data.DISTANCE[str(self.choice_central.currentText())][str(self.choice_sat.currentText())]))
    def ok(self):
        if data.MASS[str(self.choice_central.currentText())] < data.MASS[str(self.choice_sat.currentText())]:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Wahl nicht möglich")
            msg.setWindowTitle("Fehler")
            msg.exec()
        else:
            self.fill()
            self.close()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, parent = None, **kwargs):
        super(MainWindow, self).__init__(*args, parent, **kwargs)
        uic.loadUi("entry.ui", self)
        self.setWindowIcon(QtGui.QIcon("icon.gif"))
        self.examples = Examples(parent = self)
        self.settings = Settings(parent = self)
        self.b_ok.clicked.connect(lambda: self.open_vpython())
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

    def open_vpython(self):

        vp.sphere()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
