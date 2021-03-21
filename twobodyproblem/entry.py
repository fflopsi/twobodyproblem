import os
import sys
from pathlib import Path

import vpython as vp
import yaml
from PySide6 import QtGui, QtWidgets, QtCore, QtUiTools

from twobodyproblem import examples
from twobodyproblem import settings
from twobodyproblem.visualization import simulation


class MainWindow(QtWidgets.QMainWindow):
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
        super(MainWindow, self).__init__(*args, parent, **kwargs)
        self.debug = debug
        self.directory = os.path.dirname(os.path.realpath(__file__))
        if self.debug:
            print(self.directory)
        self.ui = QtUiTools.QUiLoader().load(
            QtCore.QFile(self.directory + "/ui/entry.ui"))
        self.ui.setWindowIcon(QtGui.QIcon(self.directory + "/ui/icon.gif"))
        # create other windows
        self.w_examples = examples.Examples(parent=self)
        self.w_settings = settings.Settings(parent=self)

        # add button and action functionality
        self.ui.b_ok.clicked.connect(self.open_vpython)
        self.ui.b_reset.clicked.connect(self.clear_fields)
        self.ui.actionVerlassen.triggered.connect(self.ui.close)
        self.ui.actionNeu_starten.triggered.connect(self.restart)
        self.ui.actiongespeicherte_Werte_laden.triggered.connect(
            self.load_values)
        self.ui.actionWertedatei_oeffnen.triggered.connect(
            self.load_values_dialog)
        self.ui.actionWerte_speichern.triggered.connect(self.save_values)
        self.ui.actionWertedatei_speichern_unter.triggered.connect(
            self.save_values_as)
        self.ui.actionVoreinstellungen.triggered.connect(
            self.w_examples.ui.show)
        self.ui.actionEinstellungen.triggered.connect(self.w_settings.ui.show)
        # set the tab for central as "default"
        self.ui.tabWidget.setCurrentIndex(0)

        # load presets
        self.presets: list
        with open(self.directory + "/saved_data/presets.yml", "r") as f:
            self.presets = yaml.load(f, Loader=yaml.FullLoader)
        # values needed during simulation
        self.pause = False
        self.pause_sim: vp.button
        # constants needed for calculations
        self.CENTRAL_MASS = 1.0
        self.CENTRAL_RADIUS = 1.0
        self.SAT_MASS = 1.0
        self.SAT_RADIUS = 1.0
        self.DISTANCE = 1.0
        self.SAT_v0 = vp.vector(0, 0, 0)
        self.CENTRAL_v0 = vp.vector(0, 0, 0)

    def restart(self):
        """restart the program"""
        os.execl(sys.executable, sys.executable, *sys.argv)

    def read(self):
        """make all the entered values accessible"""
        try:  # check if correct number entered
            float(self.ui.central_mass.text())
        except ValueError:  # enter standard value if an error occurs
            self.ui.central_mass.setText(str(self.presets["mass"]["Erde"]))
        finally:  # save entered value for simulation
            self.CENTRAL_MASS = float(self.ui.central_mass.text())

        try:
            float(self.ui.central_radius.text())
        except ValueError:
            self.ui.central_radius.setText(str(self.presets["radius"]["Erde"]))
        finally:
            self.CENTRAL_RADIUS = float(self.ui.central_radius.text())

        try:
            float(self.ui.sat_mass.text())
        except ValueError:
            self.ui.sat_mass.setText(str(self.presets["mass"]["Sputnik 2"]))
        finally:
            self.SAT_MASS = float(self.ui.sat_mass.text())

        try:
            float(self.ui.sat_radius.text())
        except ValueError:
            self.ui.sat_radius.setText(
                str(self.presets["radius"]["Sputnik 2"]))
        finally:
            self.SAT_RADIUS = float(self.ui.sat_radius.text())

        try:
            float(self.ui.distance.text())
        except ValueError:
            self.ui.distance.setText(
                str(self.presets["distance"]["Erde"]["Sputnik 2"]))
        finally:
            self.DISTANCE = float(self.ui.distance.text())

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
        finally:
            self.SAT_v0 = vp.vector(
                float(self.ui.sat_v0_x.text()),
                float(self.ui.sat_v0_y.text()),
                float(self.ui.sat_v0_z.text())
            )

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
        finally:
            self.CENTRAL_v0 = vp.vector(
                float(self.ui.central_v0_x.text()),
                float(self.ui.central_v0_y.text()),
                float(self.ui.central_v0_z.text())
            )

    def clear_fields(self):
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

    def values_to_dict(self) -> dict:
        """packs all entered values in a dictionary

        returns: dict
        """
        self.read()
        values = {
            "central_mass": self.CENTRAL_MASS,
            "central_radius": self.CENTRAL_RADIUS,
            "sat_mass": self.SAT_MASS,
            "sat_radius": self.SAT_RADIUS,
            "distance": self.DISTANCE,
            "sat_v0": {
                "x": self.SAT_v0.x,
                "y": self.SAT_v0.y,
                "z": self.SAT_v0.z
            },
            "central_v0": {
                "x": self.CENTRAL_v0.x,
                "y": self.CENTRAL_v0.y,
                "z": self.CENTRAL_v0.z
            }
        }
        return values

    def save_values(self):
        """save values into standard file"""
        with open(self.directory + "/saved_data/values.yml", "w+") as f:
            f.write(yaml.dump(self.values_to_dict()))

    def save_values_as(self):
        """save values to file with QFileDialog"""
        name = QtWidgets.QFileDialog.getSaveFileName(
            parent=self, caption="Eingaben speichern",
            dir=str(Path.home()) + "/Documents", filter="YAML (*.yml)")
        if name[0] != "":
            with open(name[0], "w+") as f:
                f.write(yaml.dump(self.values_to_dict()))

    def fill_values(self, val: dict):
        """fill in the given values

        args:
            val: dictionary of values to be filled in
        """
        try:
            self.ui.central_mass.setText(str(val["central_mass"]))
            self.ui.central_radius.setText(str(val["central_radius"]))
            self.ui.sat_mass.setText(str(val["sat_mass"]))
            self.ui.sat_radius.setText(str(val["sat_radius"]))
            self.ui.distance.setText(str(val["distance"]))
            self.ui.sat_v0_x.setText(str(val["sat_v0"]["x"]))
            self.ui.sat_v0_y.setText(str(val["sat_v0"]["y"]))
            self.ui.sat_v0_z.setText(str(val["sat_v0"]["z"]))
            self.ui.central_v0_x.setText(str(val["central_v0"]["x"]))
            self.ui.central_v0_y.setText(str(val["central_v0"]["y"]))
            self.ui.central_v0_z.setText(str(val["central_v0"]["z"]))
        except (TypeError, KeyError):
            err = QtWidgets.QMessageBox()
            err.setIcon(QtWidgets.QMessageBox.Critical)
            err.setText("Werte-Datei fehlerhaft")
            err.setWindowTitle("Fehler")
            err.exec()

    def load_values(self):
        """loading and filling in saved values"""
        # try to load the value file
        try:
            with open(self.directory + "/saved_data/values.yml", "r") as f:
                values = yaml.load(f, Loader=yaml.FullLoader)
                self.fill_values(values)
        except FileNotFoundError:
            err = QtWidgets.QMessageBox()
            err.setIcon(QtWidgets.QMessageBox.Critical)
            err.setText("keine gespeicherten Werte vorhanden")
            err.setWindowTitle("Fehler")
            err.exec()

    def load_values_dialog(self):
        """loading saved values with QFileDialog"""
        name = QtWidgets.QFileDialog.getOpenFileName(
            parent=self, caption="Wertedatei öffnen",
            dir=str(Path.home()) + "/Documents", filter="YAML (*.yml))"
        )
        if name[0] != "":
            with open(name[0], "r") as f:
                values = yaml.load(f, Loader=yaml.FullLoader)
                self.fill_values(values)

    def open_vpython(self):
        """open vpython window with entered values

        *to be replaced*
        """
        # read values and set up variables
        self.read()
        options = {  # create the new settings content with the entered values
            "canvas": {
                "width": self.w_settings.ui.canvas_width.value(),
                "height": self.w_settings.ui.canvas_height.value()
            },
            "do_restart": int(self.w_settings.ui.do_restart.isChecked()),
            "do_testing": int(self.w_settings.ui.do_testing.isChecked()),
            "do_central_centered": int(
                self.w_settings.ui.do_central_centered.isChecked()),
            "color": {
                "objects": {
                    "r": self.w_settings.ui.color_objects_r.value(),
                    "g": self.w_settings.ui.color_objects_g.value(),
                    "b": self.w_settings.ui.color_objects_b.value()
                },
                "pointer": {
                    "r": self.w_settings.ui.color_pointer_r.value(),
                    "g": self.w_settings.ui.color_pointer_g.value(),
                    "b": self.w_settings.ui.color_pointer_b.value()
                }
            },
            "show_pointers": int(self.w_settings.ui.show_pointers.isChecked()),
            "update_rate": self.w_settings.ui.update_rate.value(),
            "max_seconds": self.w_settings.ui.max_seconds.value(),
            "t_factor": self.w_settings.ui.t_factor.value(),
        }
        sim = simulation.Simulation(
            values=self.values_to_dict(), options=options)
        sim.start()
