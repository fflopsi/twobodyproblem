import yaml
import os
from PySide6 import QtWidgets, QtUiTools, QtCore


class Examples(QtWidgets.QMainWindow):
    """window for presets"""

    def __init__(self, *args, parent=None, **kwargs):
        # set up UI
        super(Examples, self).__init__(*args, parent, **kwargs)
        self.directory = os.path.dirname(os.path.realpath(__file__))
        self.ui = QtUiTools.QUiLoader().load(
            QtCore.QFile(self.directory + "/ui/examples.ui"))
        self.ui.actionVerlassen.triggered.connect(self.ui.close)
        self.ui.b_cancel.clicked.connect(self.ui.close)
        self.ui.b_ok.clicked.connect(lambda: (self.fill(), self.ui.close()))
        self.ui.b_fill.clicked.connect(self.fill)

        with open(self.directory + "/saved_data/presets.yml", "r") as f:
            self.values = yaml.load(f, Loader=yaml.FullLoader)

    def fill(self):
        """fill entry window fields with selected values"""
        # if satellite mass is bigger than central mass
        if self.values["mass"][str(self.ui.choice_central.currentText())] < self.values["mass"][str(self.ui.choice_sat.currentText())]:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText(
                "Zentralmasse kleiner als Zweitmasse\nEmpfehlung: bewegter Zentralkörper")
            msg.setWindowTitle("Warnung")
            msg.exec()  # show a warning message box
        # fill in the requested values
        self.parent().ui.central_mass.setText(
            str(self.values["mass"]
                [str(self.ui.choice_central.currentText())]))
        self.parent().ui.central_radius.setText(
            str(self.values["radius"]
                [str(self.ui.choice_central.currentText())]))
        self.parent().ui.sat_mass.setText(
            str(self.values["mass"][str(self.ui.choice_sat.currentText())]))
        self.parent().ui.sat_radius.setText(
            str(self.values["radius"][str(self.ui.choice_sat.currentText())]))
        self.parent().ui.distance.setText(
            str(self.values["distance"]
                [str(self.ui.choice_central.currentText())]
                [str(self.ui.choice_sat.currentText())]))
