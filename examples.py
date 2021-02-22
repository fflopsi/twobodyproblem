import yaml
from PyQt5 import uic, QtCore, QtGui, QtWidgets


class Examples(QtWidgets.QMainWindow):
    """window for presets"""

    def __init__(self, presets, *args, parent=None, **kwargs):
        super(Examples, self).__init__(*args, parent, **kwargs)  # set up UI
        examples = uic.loadUi("ui/examples.ui", self)
        self.actionVerlassen.triggered.connect(self.close)
        self.b_cancel.clicked.connect(self.close)
        self.b_ok.clicked.connect(self.ok)
        self.b_fill.clicked.connect(self.fill)

        self.values = presets

    def fill(self):
        """fill entry window fields with selected values"""
        # if satellite mass is bigger than central mass
        if self.values["mass"][str(self.choice_central.currentText())] < self.values["mass"][str(self.choice_sat.currentText())]:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText(
                "Zentralmasse kleiner als Zweitmasse\nEmpfehlung: bewegter Zentralkörper")
            msg.setWindowTitle("Warnung")
            msg.exec()  # show an error message box
        else:
            self.parent().central_mass.setText(
                str(self.values["mass"]
                    [str(self.choice_central.currentText())]))
            self.parent().central_radius.setText(
                str(self.values["radius"]
                    [str(self.choice_central.currentText())]))
            self.parent().sat_mass.setText(
                str(self.values["mass"][str(self.choice_sat.currentText())]))
            self.parent().sat_radius.setText(
                str(self.values["radius"][str(self.choice_sat.currentText())]))
            self.parent().distance.setText(
                str(self.values["distance"]
                    [str(self.choice_central.currentText())]
                    [str(self.choice_sat.currentText())]))

    def ok(self):
        """perform fill() and close window if no error occurred"""
        self.fill()
        self.close()
