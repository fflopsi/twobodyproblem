import os

from PySide6 import QtWidgets, QtUiTools, QtCore

from twobodyproblem import preset


class ExamplesWindow(QtWidgets.QMainWindow):
    """window for presets

    inherits from: QtWidgets.QMainWindow
    """

    def __init__(self, *args, parent=None, debug=False, **kwargs):
        """constructor extends QtWidgets.QMainWindow constructor

        args:
            parent: parent window (default None)
            debug: true if should be run in debug mode (default False)
            *args and **kwargs: additional args to be passed
        """
        # set up UI
        super(ExamplesWindow, self).__init__(*args, parent, **kwargs)
        self.parent = parent
        self.debug = debug
        self.directory = os.path.dirname(os.path.realpath(__file__))
        self.ui = QtUiTools.QUiLoader().load(
            QtCore.QFile(self.directory + "/ui/examples.ui"))
        self.ui.actionVerlassen.triggered.connect(self.ui.close)
        self.ui.b_cancel.clicked.connect(self.ui.close)
        self.ui.b_ok.clicked.connect(lambda: (self.fill(), self.ui.close()))
        self.ui.b_fill.clicked.connect(self.fill)

    def fill(self):
        """fill entry window fields with selected values"""
        self.parent.ui.central_mass.setText(str(preset.mass(
            self.ui.choice_central.currentText())))
        self.parent.ui.central_radius.setText(str(preset.radius(
            self.ui.choice_central.currentText())))
        self.parent.ui.sat_mass.setText(str(preset.mass(
            self.ui.choice_sat.currentText())))
        self.parent.ui.sat_radius.setText(str(preset.radius(
            self.ui.choice_sat.currentText())))
        self.parent.ui.distance.setText(str(preset.distance(
            self.ui.choice_distance.currentText())))
