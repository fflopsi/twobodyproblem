'''
Created on 23.06.2020
@author: flori
'''

import sys
import vpython as vp
from PyQt5 import uic, QtCore, QtGui, QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi("entry.ui", self)
        self.b_reset.clicked.connect(self.clear_fields)

    def clear_fields(self):
        self.central_radius.setText("")
        self.central_mass.setText("")
        self.sat_mass.setText("")
        self.sat_radius.setText("")
        self.distance.setText("")

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
