import data
from PyQt5 import uic, QtCore, QtGui, QtWidgets

class Examples(QtWidgets.QMainWindow):
    """window for presets"""
    def __init__(self, *args, parent=None, **kwargs):
        super(Examples, self).__init__(*args, parent, **kwargs)
        examples = uic.loadUi("ui/examples.ui", self)
        self.actionVerlassen.triggered.connect(self.close)
        self.b_cancel.clicked.connect(self.close)
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
            self.parent().central_mass.setText(str(data.MASS[str(self.choice_central.currentText())]))
            self.parent().central_radius.setText(str(data.RADIUS[str(self.choice_central.currentText())]))
            self.parent().sat_mass.setText(str(data.MASS[str(self.choice_sat.currentText())]))
            self.parent().sat_radius.setText(str(data.RADIUS[str(self.choice_sat.currentText())]))
            self.parent().distance.setText(str(data.DISTANCE[str(self.choice_central.currentText())][str(self.choice_sat.currentText())]))
    def ok(self):
        """perform fill() and close window if no error occurred"""
        self.fill()
        if not error:
            self.close()
