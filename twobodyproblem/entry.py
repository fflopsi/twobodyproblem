import os
import sys
from pathlib import Path

import vpython as vp
import yaml
from PySide6 import QtGui, QtWidgets, QtCore, QtUiTools

from twobodyproblem.examples import ExamplesWindow
from twobodyproblem.settings import SettingsWindow
from twobodyproblem.visualization.simulation import Simulation
from twobodyproblem.values import Values


class EntryWindow(QtWidgets.QMainWindow):
    """main window for inputs

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
        super(EntryWindow, self).__init__(*args, parent, **kwargs)
        self.debug = debug
        self.directory = os.path.dirname(os.path.realpath(__file__))
        if self.debug:
            print(self.directory)
        self.ui = QtUiTools.QUiLoader().load(
            QtCore.QFile(self.directory + "/ui/entry.ui"))
        self.ui.setWindowIcon(QtGui.QIcon(self.directory + "/ui/icon.gif"))
        # create other windows
        self.w_examples = ExamplesWindow(parent=self)
        self.w_settings = SettingsWindow(parent=self)

        # load presets
        with open(self.directory + "/saved_data/presets.yml", "r") as f:
            self.preset = yaml.load(f, Loader=yaml.FullLoader)

        # add button and action functionality
        self.ui.b_ok.clicked.connect(lambda: Simulation(
            values=self.get(),
            options=self.w_settings.get_settings()).start())
        self.ui.b_reset.clicked.connect(self.clear)
        self.ui.actionVerlassen.triggered.connect(self.ui.close)
        self.ui.actionNeu_starten.triggered.connect(self.restart)
        self.ui.actiongespeicherte_Werte_laden.triggered.connect(
            self.load)
        self.ui.actionWertedatei_oeffnen.triggered.connect(
            self.load_from)
        self.ui.actionWerte_speichern.triggered.connect(self.save)
        self.ui.actionWertedatei_speichern_unter.triggered.connect(
            self.save_as)
        self.ui.actionVoreinstellungen.triggered.connect(
            self.w_examples.ui.show)
        self.ui.actionEinstellungen.triggered.connect(self.w_settings.ui.show)
        # set the tab for central as "default"
        self.ui.tabWidget.setCurrentIndex(0)

        # values needed during simulation
        self.pause = False
        self.pause_sim: vp.button

    def restart(self):
        """restart the program"""
        os.execl(sys.executable, sys.executable, *sys.argv)

    def clear(self):
        """delete all values in all fields"""
        self.ui.central_radius.setText("")
        self.ui.central_mass.setText("")
        self.ui.sat_mass.setText("")
        self.ui.sat_radius.setText("")
        self.ui.distance.setText("")
        self.ui.sat_v0_x.setText("")
        self.ui.sat_v0_y.setText("")
        self.ui.sat_v0_z.setText("")
        self.ui.central_v0_x.setText("")
        self.ui.central_v0_y.setText("")
        self.ui.central_v0_z.setText("")

    def fill_standards(self):
        """fill in the standard values if field is empty or wrongly filled"""
        try:  # check if valid number entered
            float(self.ui.central_mass.text())
        except ValueError:  # enter standard value if an error occurs
            self.ui.central_mass.setText(str(self.preset["mass"]["Erde"]))
        try:
            float(self.ui.central_radius.text())
        except ValueError:
            self.ui.central_radius.setText(str(self.preset["radius"]["Erde"]))
        try:
            float(self.ui.central_v0_x.text())
        except ValueError:
            self.ui.central_v0_x.setText("0")
        try:
            float(self.ui.central_v0_y.text())
        except ValueError:
            self.ui.central_v0_y.setText("0")
        try:
            float(self.ui.central_v0_z.text())
        except ValueError:
            self.ui.central_v0_z.setText("0")

        try:
            float(self.ui.sat_mass.text())
        except ValueError:
            self.ui.sat_mass.setText(str(self.preset["mass"]["Sputnik 2"]))
        try:
            float(self.ui.sat_radius.text())
        except ValueError:
            self.ui.sat_radius.setText(str(self.preset["radius"]["Sputnik 2"]))
        try:
            float(self.ui.sat_v0_x.text())
        except ValueError:
            self.ui.sat_v0_x.setText("0")
        try:
            float(self.ui.sat_v0_y.text())
        except ValueError:
            self.ui.sat_v0_y.setText("0")
        try:
            float(self.ui.sat_v0_z.text())
        except ValueError:
            self.ui.sat_v0_z.setText("-8000")

        try:
            float(self.ui.distance.text())
        except ValueError:
            self.ui.distance.setText(
                str(self.preset["distance"]["Erde"]["Sputnik 2"]))

    def fill(self, val: Values):
        """fill in the given values

        args:
            val: Values to be filled in
        """
        self.ui.central_mass.setText(str(val.central.mass))
        self.ui.central_radius.setText(str(val.central.radius))
        self.ui.central_v0_x.setText(str(val.central.velocity.x))
        self.ui.central_v0_y.setText(str(val.central.velocity.y))
        self.ui.central_v0_z.setText(str(val.central.velocity.z))
        self.ui.sat_mass.setText(str(val.sat.mass))
        self.ui.sat_radius.setText(str(val.sat.radius))
        self.ui.sat_v0_x.setText(str(val.sat.velocity.x))
        self.ui.sat_v0_y.setText(str(val.sat.velocity.y))
        self.ui.sat_v0_z.setText(str(val.sat.velocity.z))
        self.ui.distance.setText(str(val.distance))

    def get(self) -> Values:
        """get the entered values for further use

        returns: Values
        """
        self.fill_standards()
        return Values(central_mass=float(self.ui.central_mass.text()),
                      central_radius=float(self.ui.central_radius.text()),
                      central_v0_x=float(self.ui.central_v0_x.text()),
                      central_v0_y=float(self.ui.central_v0_y.text()),
                      central_v0_z=float(self.ui.central_v0_z.text()),
                      sat_mass=float(self.ui.sat_mass.text()),
                      sat_radius=float(self.ui.sat_radius.text()),
                      sat_v0_x=float(self.ui.sat_v0_x.text()),
                      sat_v0_y=float(self.ui.sat_v0_y.text()),
                      sat_v0_z=float(self.ui.sat_v0_z.text()),
                      distance=float(self.ui.distance.text()))

    def save(self):
        """save values into standard file"""
        with open(self.directory + "/saved_data/values.yml", "w+") as f:
            f.write(yaml.dump(self.get().to_dict()))

    def save_as(self):
        """save values to file with QFileDialog"""
        name = QtWidgets.QFileDialog.getSaveFileName(
            parent=self, caption="Eingaben speichern",
            dir=str(Path.home()) + "/Documents", filter="YAML (*.yml)")
        if name[0] != "":
            with open(name[0], "w+") as f:
                f.write(yaml.dump(self.get().to_dict()))

    def load(self):
        """loading and filling in saved values"""
        # try to load the value file
        try:
            with open(self.directory + "/saved_data/values.yml", "r") as f:
                self.fill(Values.from_dict(
                    yaml.load(f, Loader=yaml.FullLoader)))
        except FileNotFoundError:
            err = QtWidgets.QMessageBox()
            err.setIcon(QtWidgets.QMessageBox.Critical)
            err.setText("keine gespeicherten Werte vorhanden")
            err.setWindowTitle("Fehler")
            err.exec()

    def load_from(self):
        """loading saved values with QFileDialog"""
        name = QtWidgets.QFileDialog.getOpenFileName(
            parent=self, caption="Wertedatei öffnen",
            dir=str(Path.home()) + "/Documents", filter="YAML (*.yml))"
        )
        if name[0] != "":
            with open(name[0], "r") as f:
                self.fill(Values.from_dict(
                    yaml.load(f, Loader=yaml.FullLoader)))
