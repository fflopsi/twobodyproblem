from twobodyproblem import settings
from twobodyproblem import examples
from twobodyproblem.visualization import simulation
import sys
import os
import signal
import yaml
import vpython as vp
from PySide6 import QtGui, QtWidgets, QtCore, QtUiTools


class MainWindow(QtWidgets.QMainWindow):
    """main window for inputs"""

    def __init__(self, *args, parent=None, **kwargs):
        # set up UI
        super(MainWindow, self).__init__(*args, parent, **kwargs)
        self.directory = os.path.dirname(os.path.realpath(__file__))
        self.ui = QtUiTools.QUiLoader().load(
            QtCore.QFile(self.directory + "/ui/entry.ui"))
        self.ui.setWindowIcon(QtGui.QIcon(self.directory + "/ui/icon.gif"))
        # create other windows
        self.w_examples = examples.Examples(parent=self)
        self.w_settings = settings.Settings(parent=self)

        # add button and action funcionality
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

        self.presets: list
        with open(self.directory + "/saved_data/presets.yml", "r") as f:
            self.presets = yaml.load(f, Loader=yaml.FullLoader)
        # values needed during simulation
        self.pause = False
        self.pause_sim: vp.button
        # constants needed for calculations
        self.CENTRAL_MASS: float
        self.CENTRAL_RADIUS: float
        self.SAT_MASS: float
        self.SAT_RADIUS: float
        self.DISTANCE: float
        self.SAT_v0: vp.vector
        self.CENTRAL_v0: vp.vector
        # vpython objects for simulation
        self.central: vp.sphere
        self.sat: vp.sphere
        if self.w_settings.ui.show_pointers.isChecked():
            self.central_pointer: vp.arrow
            self.sat_pointer: vp.arrow
        self.central_radius_smaller: vp.slider
        self.central_radius_bigger: vp.slider
        self.sat_radius_smaller: vp.slider
        self.sat_radius_bigger: vp.slider

        if self.w_settings.ui.do_central_unmoving.isChecked():
            self.ui.central_v0_x.setEnabled(False)
            self.ui.central_v0_y.setEnabled(False)
            self.ui.central_v0_z.setEnabled(False)

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
        """returns the entered values as dictionary"""
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
        """save values to file with SaveFile dialog"""
        name = QtWidgets.QFileDialog.getSaveFileName(
            parent=self, caption="Eingaben speichern",
            dir="saved_data", filter="YAML (*.yml)")
        if name[0] != "":
            with open(name[0], "w+") as f:
                f.write(yaml.dump(self.values_to_dict()))

    def fill_in_dict(self, val: dict):
        """fill in the given values"""
        try:
            self.ui.central_mass.setText(str(val["central_mass"]))
            self.ui.central_radius.setText(str(val["central_radius"]))
            self.ui.sat_mass.setText(str(val["sat_mass"]))
            self.ui.sat_radius.setText(str(val["sat_radius"]))
            self.ui.distance.setText(str(val["distance"]))
            self.ui.sat_v0_x.setText(str(val["sat_v0"]["x"]))
            self.ui.sat_v0_y.setText(str(val["sat_v0"]["y"]))
            self.ui.sat_v0_z.setText(str(val["sat_v0"]["z"]))
            if not self.w_settings.ui.do_central_unmoving.isChecked():
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
                self.fill_in_dict(values)
        except FileNotFoundError:
            err = QtWidgets.QMessageBox()
            err.setIcon(QtWidgets.QMessageBox.Critical)
            err.setText("keine gespeicherten Werte vorhanden")
            err.setWindowTitle("Fehler")
            err.exec()

    def load_values_dialog(self):
        """loading saved values with "open file" dialog"""
        name = QtWidgets.QFileDialog.getOpenFileName(
            parent=self, caption="Wertedatei öffnen",
            dir="saved_data", filter="YAML (*.yml))"
        )
        if name[0] != "":
            with open(name[0], "r") as f:
                values = yaml.load(f, Loader=yaml.FullLoader)
                self.fill_in_dict(values)

    def pause_simulation(self):
        """pause or un-pause the simulation"""
        self.pause = not self.pause
        if self.pause:
            self.pause_sim.text = "Play"
        else:
            self.pause_sim.text = "Pause"

    def adjust_central_radius(self, value):
        """adjust radius of central (and pointer if needed)"""
        self.central.radius = self.CENTRAL_RADIUS * value
        if self.w_settings.ui.show_pointers.isChecked():
            self.central_pointer.pos = self.central.pos - \
                self.central_pointer.axis + \
                vp.vector(0, self.central.radius, 0)

    def reset_central_radius_slider(self):
        """reset the central radius sliders"""
        self.central_radius_smaller.value = 1
        self.central_radius_bigger.value = 1
        self.adjust_central_radius(value=1)

    def adjust_sat_radius(self, value):
        """adjust radius of sat (and pointer if needed)"""
        self.sat.radius = self.SAT_RADIUS * value
        if self.w_settings.ui.show_pointers.isChecked():
            self.sat_pointer.pos = self.sat.pos - \
                self.sat_pointer.axis + vp.vector(0, self.sat.radius, 0)

    def reset_sat_radius_slider(self):
        """reset the sat radius sliders"""
        self.sat_radius_slider_smaller.value = 1
        self.sat_radius_bigger.value = 1
        self.adjust_sat_radius(value=1)

    def open_vpython(self):
        """open vpython window with entered values"""
        # read values and set up variables
        self.read()
        testing = self.w_settings.ui.do_testing.isChecked()
        if testing:
            options = {  # create the new settings content with the entered values
                "canvas": {
                    "width": self.w_settings.ui.canvas_width.value(),
                    "height": self.w_settings.ui.canvas_height.value()
                },
                "do_restart": int(self.w_settings.ui.do_restart.isChecked()),
                "do_testing": int(self.w_settings.ui.do_testing.isChecked()),
                "do_central_unmoving": int(self.w_settings.ui.do_central_unmoving.isChecked()),
                "do_central_centered": int(self.w_settings.ui.do_central_centered.isChecked()),
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
                window=self, values=self.values_to_dict(), options=options)
            sim.start()
        else:
            t = 0
            t_max = self.w_settings.ui.update_rate.value() * \
                self.w_settings.ui.max_seconds.value()
            central_unmoving = self.w_settings.ui.do_central_unmoving.isChecked()
            central_centered = self.w_settings.ui.do_central_centered.isChecked()

            # set up vpython canvas, objects and pointers (arrows to the objects because the scales are too large)
            scene = vp.canvas(
                title="Simulation zum Zweikörperproblem",
                height=self.w_settings.ui.canvas_height.value(),
                width=self.w_settings.ui.canvas_width.value()
            )
            self.central = vp.sphere(
                radius=self.CENTRAL_RADIUS, make_trail=True,
                color=vp.vector(
                    self.w_settings.ui.color_objects_r.value()/255,
                    self.w_settings.ui.color_objects_g.value()/255,
                    self.w_settings.ui.color_objects_b.value()/255
                )
            )
            self.sat = vp.sphere(
                pos=vp.vector(self.DISTANCE + self.SAT_RADIUS + self.CENTRAL_RADIUS, 0, 0),
                radius=self.SAT_RADIUS, make_trail=True,
                color=vp.vector(
                    self.w_settings.ui.color_objects_r.value()/255,
                    self.w_settings.ui.color_objects_g.value()/255,
                    self.w_settings.ui.color_objects_b.value()/255
                )
            )
            if self.w_settings.ui.show_pointers.isChecked():
                self.central_pointer = vp.arrow(
                    axis=vp.vector(0, -(self.DISTANCE / 2), 0),
                    color=vp.vector(
                        self.w_settings.ui.color_pointer_r.value()/255,
                        self.w_settings.ui.color_pointer_g.value()/255,
                        self.w_settings.ui.color_pointer_b.value()/255
                    )
                )
                self.central_pointer.pos = self.central.pos - self.central_pointer.axis + \
                    vp.vector(0, self.CENTRAL_RADIUS, 0)
                self.sat_pointer = vp.arrow(
                    axis=vp.vector(0, -(self.DISTANCE / 2), 0),
                    color=vp.vector(
                        self.w_settings.ui.color_pointer_r.value()/255,
                        self.w_settings.ui.color_pointer_g.value()/255,
                        self.w_settings.ui.color_pointer_b.value()/255
                    )
                )

            # set up buttons
            self.pause_sim = vp.button(
                text="Pause", bind=self.pause_simulation)
            vp.button(text="Stop", bind=lambda: os.kill(
                os.getpid(), signal.SIGINT))
            vp.button(text="Restart", bind=self.restart)
            scene.append_to_caption("\n")

            # sliders for changing the radius magnification of the two objects
            self.central_radius_smaller = vp.slider(
                min=0.01, max=1, step=0.01, value=1,
                bind=lambda: self.adjust_central_radius(
                    value=self.central_radius_smaller.value),
                top=12, bottom=12
            )
            self.central_radius_bigger = vp.slider(
                min=1, max=100, step=1, value=1,
                bind=lambda: self.adjust_central_radius(
                    value=self.central_radius_bigger.value),
                top=12, bottom=12
            )
            vp.button(text="Reset", bind=self.reset_central_radius_slider)
            scene.append_to_caption("\n")
            self.sat_radius_smaller = vp.slider(
                min=0.01, max=1, step=0.01, value=1, top=12, bottom=12,
                bind=lambda: self.adjust_sat_radius(
                    value=self.sat_radius_smaller.value)
            )
            self.sat_radius_bigger = vp.slider(
                min=1, max=100, step=1, value=1, top=12, bottom=12,
                bind=lambda: self.adjust_sat_radius(
                    value=self.sat_radius_bigger.value)
            )
            vp.button(text="Reset", bind=self.reset_sat_radius_slider)

            # some values for calculations
            G = 6.67430e-11  # gravitational constant
            M = self.CENTRAL_MASS
            m = self.SAT_MASS
            delta_t = self.w_settings.ui.t_factor.value()
            if not central_unmoving:
                pos1_s = self.sat.pos
                pos1_c = self.central.pos
                v_pos1_s = self.SAT_v0
                v_pos1_c = self.CENTRAL_v0
            else:
                pos1 = self.sat.pos
                v_pos1 = self.SAT_v0

            if central_centered:
                scene.camera.follow(self.central)

            if testing:
                vp.attach_arrow(self.sat, "axis", scale=1e4)
                vp.attach_arrow(self.central, "axis", scale=1e4)

            # movement while simulation time not over
            while t < t_max:
                if not self.pause:
                    vp.rate(self.w_settings.ui.update_rate.value())
                    r = self.sat.pos - self.central.pos
                    if not central_unmoving:
                        # calculations of force, acceleration and velocity: _s for sat, _c for central
                        F_s = ((G*M*m) / (vp.mag(r)**2)) * vp.norm(-r)
                        F_c = ((G*M*m) / (vp.mag(r)**2)) * vp.norm(r)
                        a_s = F_s / m
                        a_c = F_c / M
                        v_s = a_s*delta_t + v_pos1_s
                        v_c = a_c*delta_t + v_pos1_c

                        # move sat, central (and pointers if needed) to new positions
                        self.sat.pos = v_s*delta_t + pos1_s
                        if testing:
                            self.sat.axis = v_s
                            self.central.axis = v_c
                        self.central.pos = v_c*delta_t + pos1_c
                        if self.w_settings.ui.show_pointers.isChecked():
                            self.sat_pointer.pos = self.sat.pos - \
                                self.sat_pointer.axis + \
                                vp.vector(0, self.sat.radius, 0)
                            self.central_pointer.pos = self.central.pos - \
                                self.central_pointer.axis + \
                                vp.vector(0, self.central.radius, 0)

                        # make the current velocities and positions available for next iteration
                        v_pos1_s = v_s
                        v_pos1_c = v_c
                        pos1_s = self.sat.pos
                        pos1_c = self.central.pos
                    else:  # same as above but only for sat
                        F = ((G*M*m) / (vp.mag(r)**2)) * vp.norm(-r)
                        a = F / m
                        v = a*delta_t + v_pos1
                        self.sat.pos = v*delta_t + pos1

                        v_pos1 = v
                        pos1 = self.sat.pos
                        if self.w_settings.ui.show_pointers.isChecked():
                            self.sat_pointer.pos = self.sat.pos - \
                                self.sat_pointer.axis + \
                                vp.vector(0, self.sat.radius, 0)

                    t += 1

            if self.w_settings.ui.do_restart.isChecked():
                self.restart()
