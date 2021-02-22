import sys
import examples
import settings
import os
import signal
import yaml
import vpython as vp
from PyQt5 import uic, QtCore, QtGui, QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    """main window for inputs"""
    EXIT_CODE_REBOOT = -123

    def __init__(self, *args, parent=None, **kwargs):
        # set up UI
        super(MainWindow, self).__init__(*args, parent, **kwargs)
        uic.loadUi("ui/input.ui", self)
        self.setWindowIcon(QtGui.QIcon("ui/icon.gif"))
        self.presets = list()
        with open("saved_data/presets.yml", "r") as f:
            presets = yaml.load(f, Loader=yaml.FullLoader)
        # create other windows
        self.examples = examples.Examples(presets=presets, parent=self)
        self.settings = settings.Settings(parent=self)

        # add button and action funcionality
        self.b_ok.clicked.connect(self.open_vpython)
        self.b_reset.clicked.connect(self.clear_fields)
        self.actionVerlassen.triggered.connect(self.close)
        self.actiongespeicherte_Werte_laden.triggered.connect(self.load_values)
        self.actionVoreinstellungen.triggered.connect(self.examples.show)
        self.actionEinstellungen.triggered.connect(self.settings.show)
        # set the tab for central as "default"
        self.tabWidget.setCurrentIndex(0)

        # values needed during simulation
        self.pause = False
        self.pause_sim = 0
        # constants needed for calculations
        self.CENTRAL_MASS = 0
        self.CENTRAL_RADIUS = 0
        self.SAT_MASS = 0
        self.SAT_RADIUS = 0
        self.DISTANCE = 0
        self.SAT_v0 = vp.vector(0, 0, 0)
        self.CENTRAL_v0 = vp.vector(0, 0, 0)
        # vpython objects for simulation
        self.central = 0
        self.sat = 0
        if self.settings.show_pointers.isChecked():
            self.central_pointer = 0
            self.sat_pointer = 0
        self.central_radius_slider_smaller = 0
        self.central_radius_slider_bigger = 0
        self.sat_radius_slider_smaller = 0
        self.sat_radius_slider_bigger = 0

        if self.settings.do_central_unmoving.isChecked():
            self.central_v0_x.setEnabled(False)
            self.central_v0_y.setEnabled(False)
            self.central_v0_z.setEnabled(False)

    def restart(self):
        """restart the program after simulation has finished"""
        os.execl(sys.executable, sys.executable, *sys.argv)
        # another option (not recommended):
        # QtWidgets.QApplication.exit(MainWindow.EXIT_CODE_REBOOT)

    def read(self):
        """make all the entered values globally accessible"""
        try:  # check if correct number entered
            float(self.central_mass.text())
        except ValueError:  # enter standard value if an error occurs
            self.central_mass.setText(str(presets["mass"]["Erde"]))
        finally:  # save entered value for simulation
            self.CENTRAL_MASS = float(self.central_mass.text())

        try:
            float(self.central_radius.text())
        except ValueError:
            self.central_radius.setText(str(presets["radius"]["Erde"]))
        finally:
            self.CENTRAL_RADIUS = float(self.central_radius.text())

        try:
            float(self.sat_mass.text())
        except ValueError:
            self.sat_mass.setText(str(presets["mass"]["Sputnik 2"]))
        finally:
            self.SAT_MASS = float(self.sat_mass.text())

        try:
            float(self.sat_radius.text())
        except ValueError:
            self.sat_radius.setText(str(presets["radius"]["Sputnik 2"]))
        finally:
            self.SAT_RADIUS = float(self.sat_radius.text())

        try:
            float(self.distance.text())
        except ValueError:
            self.distance.setText(
                str(presets["distance"]["Erde"]["Sputnik 2"]))
        finally:
            self.DISTANCE = float(self.distance.text()) + \
                self.CENTRAL_RADIUS + self.SAT_RADIUS  # so lassen?

        try:
            float(self.sat_v0_x.text())
        except ValueError:
            self.sat_v0_x.setText("0")
        try:
            float(self.sat_v0_y.text())
        except ValueError:
            self.sat_v0_y.setText("0")
        try:
            float(self.sat_v0_z.text())
        except ValueError:
            self.sat_v0_z.setText("-8000")
        finally:
            self.SAT_v0 = vp.vector(
                float(self.sat_v0_x.text()),
                float(self.sat_v0_y.text()),
                float(self.sat_v0_z.text())
            )

        try:
            float(self.central_v0_x.text())
        except ValueError:
            self.central_v0_x.setText("0")
        try:
            float(self.central_v0_y.text())
        except ValueError:
            self.central_v0_y.setText("0")
        try:
            float(self.central_v0_z.text())
        except ValueError:
            self.central_v0_z.setText("0")
        finally:
            self.CENTRAL_v0 = vp.vector(
                float(self.central_v0_x.text()),
                float(self.central_v0_y.text()),
                float(self.central_v0_z.text())
            )

        if self.save_values.isChecked():
            with open("saved_data/values.yml", "w+") as f:
                values = {
                    "central_mass": self.CENTRAL_MASS,
                    "central_radius": self.CENTRAL_RADIUS,
                    "sat_mass": self.SAT_MASS,
                    "sat_radius": self.SAT_RADIUS,
                    "distance": self.DISTANCE - self.CENTRAL_RADIUS - self.SAT_RADIUS,
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
                f.write(yaml.dump(values))

    def clear_fields(self):
        """delete all values in all fields"""
        self.central_radius.setText("")
        self.central_mass.setText("")
        self.sat_mass.setText("")
        self.sat_radius.setText("")
        self.distance.setText("")
        self.sat_v0_x.setText("")
        self.sat_v0_y.setText("")
        self.sat_v0_z.setText("")
        self.central_v0_x.setText("")
        self.central_v0_y.setText("")
        self.central_v0_z.setText("")

    def load_values(self):
        """loading and filling in saved values"""
        # set up the message box
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setText(
            "Möchten Sie die gespeicherten Werte löschen oder behalten?")
        msg.setWindowTitle("gespeicherte Werte laden")
        msg.setStandardButtons(QtWidgets.QMessageBox.Save |
                               QtWidgets.QMessageBox.Discard |
                               QtWidgets.QMessageBox.Cancel)
        msg.button(QtWidgets.QMessageBox.Save).setText("Behalten")
        msg.button(QtWidgets.QMessageBox.Discard).setText("Löschen")
        msg.button(QtWidgets.QMessageBox.Cancel).setText("Abbrechen")
        msg.setDefaultButton(QtWidgets.QMessageBox.Save)
        msg.setEscapeButton(QtWidgets.QMessageBox.Cancel)

        res = msg.exec()
        if res == QtWidgets.QMessageBox.Save or res == QtWidgets.QMessageBox.Discard:
            # try to load the requested value file
            values = list()
            try:
                with open("saved_data/values.yml", "r") as f:
                    values = yaml.load(f, Loader=yaml.FullLoader)
                if msg.clickedButton() == QtWidgets.QMessageBox.Discard:
                    os.remove("saved_data/values.yml")
                # try to fill in all values
                try:
                    self.central_mass.setText(str(values["central_mass"]))
                    self.central_radius.setText(str(values["central_radius"]))
                    self.sat_mass.setText(str(values["sat_mass"]))
                    self.sat_radius.setText(str(values["sat_radius"]))
                    self.distance.setText(str(values["distance"]))
                    self.sat_v0_x.setText(str(values["sat_v0"]["x"]))
                    self.sat_v0_y.setText(str(values["sat_v0"]["y"]))
                    self.sat_v0_z.setText(str(values["sat_v0"]["z"]))
                    if not self.settings.do_central_unmoving.isChecked():
                        self.central_v0_x.setText(str(values["central_v0"]["x"]))
                        self.central_v0_y.setText(str(values["central_v0"]["y"]))
                        self.central_v0_z.setText(str(values["central_v0"]["z"]))
                except TypeError:
                    err = QtWidgets.QMessageBox()
                    err.setIcon(QtWidgets.QMessageBox.Critical)
                    err.setText("Werte-Datei fehlerhaft")
                    err.setWindowTitle("Fehler")
                    err.exec()
            except FileNotFoundError:
                error = True
                err = QtWidgets.QMessageBox()
                err.setIcon(QtWidgets.QMessageBox.Critical)
                err.setText("keine gespeicherten Werte vorhanden")
                err.setWindowTitle("Fehler")
                err.exec()

    def pause_simulation(self):
        """pause the simulation"""
        self.pause = not self.pause
        if self.pause:
            self.pause_sim.text = "Play"
        else:
            self.pause_sim.text = "Pause"

    def adjust_central_radius(self, value):
        """adjust radius of central (and pointer if needed)"""
        self.central.radius = self.CENTRAL_RADIUS * value
        if self.settings.show_pointers.isChecked():
            self.central_pointer.pos = self.central.pos - \
                self.central_pointer.axis + \
                vp.vector(0, self.central.radius, 0)

    def reset_central_radius_slider(self):
        """reset the central radius sliders"""
        self.central_radius_slider_smaller.value = 1
        self.central_radius_slider_bigger.value = 1
        self.adjust_central_radius(value=1)

    def adjust_sat_radius(self, value):
        """adjust radius of sat (and pointer if needed)"""
        self.sat.radius = self.SAT_RADIUS * value
        if self.settings.show_pointers.isChecked():
            self.sat_pointer.pos = self.sat.pos - \
                self.sat_pointer.axis + vp.vector(0, self.sat.radius, 0)

    def reset_sat_radius_slider(self):
        """reset the sat radius sliders"""
        self.sat_radius_slider_smaller.value = 1
        self.sat_radius_slider_bigger.value = 1
        self.adjust_sat_radius(value=1)

    def open_vpython(self):
        """open vpython window with entered values"""
        # read values and set up variables
        self.read()
        t = 0
        t_max = self.settings.update_rate.value() * self.settings.max_seconds.value()
        testing = self.settings.do_testing.isChecked()
        central_unmoving = self.settings.do_central_unmoving.isChecked()
        central_centered = self.settings.do_central_centered.isChecked()

        # set up vpython canvas, objects and pointers (arrows to the objects because the scales are too large)
        scene = vp.canvas(
            title="Simulation zum Zweikörperproblem",
            height=self.settings.canvas_height.value(),
            width=self.settings.canvas_width.value()
        )
        self.central = vp.sphere(
            radius=self.CENTRAL_RADIUS,
            make_trail=True,
            color=vp.vector(
                self.settings.color_objects_r.value()/255,
                self.settings.color_objects_g.value()/255,
                self.settings.color_objects_b.value()/255
            )
        )
        self.sat = vp.sphere(
            pos=vp.vector(self.DISTANCE, 0, 0),
            radius=self.SAT_RADIUS,
            make_trail=True,
            color=vp.vector(
                self.settings.color_objects_r.value()/255,
                self.settings.color_objects_g.value()/255,
                self.settings.color_objects_b.value()/255
            )
        )
        if self.settings.show_pointers.isChecked():
            self.central_pointer = vp.arrow(
                axis=vp.vector(0, -(self.DISTANCE / 2), 0),
                color=vp.vector(
                    self.settings.color_pointer_r.value()/255,
                    self.settings.color_pointer_g.value()/255,
                    self.settings.color_pointer_b.value()/255
                )
            )
            self.central_pointer.pos = self.central.pos - self.central_pointer.axis + \
                vp.vector(0, self.CENTRAL_RADIUS, 0)
            self.sat_pointer = vp.arrow(
                axis=vp.vector(0, -(self.DISTANCE / 2), 0),
                color=vp.vector(
                    self.settings.color_pointer_r.value()/255,
                    self.settings.color_pointer_g.value()/255,
                    self.settings.color_pointer_b.value()/255
                )
            )

        # set up pause button
        self.pause_sim = vp.button(text="Pause", bind=self.pause_simulation)
        vp.button(text="Stop", bind=lambda: os.kill(
            os.getpid(), signal.SIGINT))
        vp.button(text="Restart", bind=self.restart)
        scene.append_to_caption("\n")

        # sliders for changing the radius magnification of the two objects
        self.central_radius_slider_smaller = vp.slider(
            min=0.01, max=1, step=0.01, value=1,
            bind=lambda: self.adjust_central_radius(
                value=self.central_radius_slider_smaller.value),
            top=12, bottom=12
        )
        self.central_radius_slider_bigger = vp.slider(
            min=1, max=100, step=1, value=1,
            bind=lambda: self.adjust_central_radius(
                value=self.central_radius_slider_bigger.value),
            top=12, bottom=12
        )
        vp.button(text="Reset", bind=self.reset_central_radius_slider)
        scene.append_to_caption("\n")
        self.sat_radius_slider_smaller = vp.slider(
            min=0.01, max=1, step=0.01, value=1,
            bind=lambda: self.adjust_sat_radius(
                value=self.sat_radius_slider_smaller.value),
            top=12, bottom=12
        )
        self.sat_radius_slider_bigger = vp.slider(
            min=1, max=100, step=1, value=1,
            bind=lambda: self.adjust_sat_radius(
                value=self.sat_radius_slider_bigger.value),
            top=12, bottom=12
        )
        vp.button(text="Reset", bind=self.reset_sat_radius_slider)

        # some values for calculations
        G = 6.67430e-11  # gravitational constant
        M = self.CENTRAL_MASS
        m = self.SAT_MASS
        delta_t = self.settings.t_factor.value()
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

        # movement while simulation time not over
        while t < t_max:
            if not self.pause:
                vp.rate(self.settings.update_rate.value())
                r = self.sat.pos - self.central.pos
                # for testing: delete "or testing" and insert testing code into else below
                if not testing or testing:
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
                        self.central.pos = v_c*delta_t + pos1_c
                        # andere Möglichkeit ausprobieren (direkt bei sat definieren)
                        if self.settings.show_pointers.isChecked():
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
                        if self.settings.show_pointers.isChecked():
                            self.sat_pointer.pos = self.sat.pos - \
                                self.sat_pointer.axis + \
                                vp.vector(0, self.sat.radius, 0)
                else:
                    # insert testing code here
                    pass

                t += 1

        if self.settings.do_restart.isChecked():
            self.restart()
