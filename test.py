'''
Created on 23.06.2020
@author: flori
'''

import sys, data
import vpython as vp
from PyQt5 import uic, QtCore, QtGui, QtWidgets

class Settings(QtWidgets.QMainWindow):
    """window for settings, no functionality yet"""
    def __init__(self, *args, parent = None, **kwargs):
        super(Settings, self).__init__(*args, parent, **kwargs)
        settings = uic.loadUi("settings.ui", self)

class Examples(QtWidgets.QMainWindow):
    """window for presets"""
    def __init__(self, *args, parent = None, **kwargs):
        super(Examples, self).__init__(*args, parent, **kwargs)
        examples = uic.loadUi("examples.ui", self)
        self.actionVerlassen.triggered.connect(self.close)
        self.b_ok.clicked.connect(self.ok)
        self.b_fill.clicked.connect(self.fill) # "Übernehmen" button

    def fill(self):
        """fill entry window fields with selected values"""
        global error
        if data.MASS[str(self.choice_central.currentText())] < data.MASS[str(self.choice_sat.currentText())]: # if satellite mass is bigger than central mass
            error = True
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Wahl nicht möglich")
            msg.setWindowTitle("Fehler")
            msg.exec() # show an error message box
        else:
            error = False
            window.central_mass.setText(str(data.MASS[str(self.choice_central.currentText())]))
            window.central_radius.setText(str(data.RADIUS[str(self.choice_central.currentText())]))
            window.sat_mass.setText(str(data.MASS[str(self.choice_sat.currentText())]))
            window.sat_radius.setText(str(data.RADIUS[str(self.choice_sat.currentText())]))
            window.distance.setText(str(data.DISTANCE[str(self.choice_central.currentText())][str(self.choice_sat.currentText())]))
    def ok(self):
        """perform fill() and close window if no error occurred"""
        self.fill()
        if not error:
            self.close()

class MainWindow(QtWidgets.QMainWindow):
    """the main window, or entry window"""
    def __init__(self, *args, parent = None, **kwargs):
        super(MainWindow, self).__init__(*args, parent, **kwargs)
        uic.loadUi("entry.ui", self)
        self.setWindowIcon(QtGui.QIcon("icon.gif"))
        self.examples = Examples(parent = self)
        self.settings = Settings(parent = self)
        self.b_ok.clicked.connect(self.open_vpython)
        self.b_reset.clicked.connect(self.clear_fields)
        self.actionListe_mit_Voreinstellungen.triggered.connect(self.examples.show)
        self.actionVerlassen.triggered.connect(app.exit)
        self.actionEinstellungen.triggered.connect(self.settings.show)

    def read(self):
        """make all the entered values accessible everywhere"""
        global central_mass
        central_mass = float(self.central_mass.text())
        global central_radius
        central_radius = float(self.central_radius.text())
        global sat_mass
        sat_mass = float(self.sat_mass.text())
        global sat_radius
        sat_radius = float(self.sat_radius.text())
        global distance
        distance = float(self.distance.text()) + central_radius + sat_radius

    def clear_fields(self):
        """delete all values in all fields"""
        self.central_radius.setText("")
        self.central_mass.setText("")
        self.sat_mass.setText("")
        self.sat_radius.setText("")
        self.distance.setText("")

    def open_vpython(self):
        """open vpython window with entered values"""
        self.read()
        central = vp.sphere(radius = central_radius)
        sat = vp.sphere(pos = vp.vector(distance,0,0), radius = sat_radius, make_trail = True)
        # pointer = vp.arrow(pos = sat.pos - )
        x = 0
        while x < 300: # simple movement
            vp.rate(30)
            sat.pos += vp.vector(distance,0,0) / 300
            x += 1

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
