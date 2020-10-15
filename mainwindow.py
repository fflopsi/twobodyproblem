import sys, data, examples, settings, os, math, scipy.constants, yaml
import vpython as vp
from PyQt5 import uic, QtCore, QtGui, QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    """the main window, or entry window"""
    def __init__(self, *args, parent=None, **kwargs):
        super(MainWindow, self).__init__(*args, parent, **kwargs)
        uic.loadUi("ui/entry.ui", self)
        self.setWindowIcon(QtGui.QIcon("ui/icon.gif"))
        self.examples = examples.Examples(parent=self)
        self.settings = settings.Settings(parent=self)
        self.actionVerlassen.triggered.connect(self.close)
        self.b_ok.clicked.connect(self.open_vpython)
        self.b_reset.clicked.connect(self.clear_fields)
        self.actiongespeicherte_Werte_laden.triggered.connect(self.load_values)
        self.actionListe_mit_Voreinstellungen.triggered.connect(self.examples.show)
        self.actionEinstellungen.triggered.connect(self.settings.show)

    def restart(self):
        """restart the program after simulation has finished"""
        os.execl(sys.executable, sys.executable, *sys.argv)

    def read(self):
        """make all the entered values globally accessible"""
        global CENTRAL_MASS
        global CENTRAL_RADIUS
        global SAT_MASS
        global SAT_RADIUS
        global DISTANCE
        global v0

        try:
            float(self.central_mass.text())
        except ValueError:
            self.central_mass.setText(str(data.MASS["Erde"]))
        finally:
            CENTRAL_MASS = float(self.central_mass.text())

        try:
            float(self.central_radius.text())
        except ValueError:
            self.central_radius.setText(str(data.RADIUS["Erde"]))
        finally:
            CENTRAL_RADIUS = float(self.central_radius.text())

        try:
            float(self.sat_mass.text())
        except ValueError:
            self.sat_mass.setText(str(data.MASS["Sputnik 2"]))
        finally:
            SAT_MASS = float(self.sat_mass.text())

        try:
            float(self.sat_radius.text())
        except ValueError:
            self.sat_radius.setText(str(data.RADIUS["Sputnik 2"]))
        finally:
            SAT_RADIUS = float(self.sat_radius.text())

        try:
            float(self.distance.text())
        except ValueError:
            self.distance.setText(str(data.DISTANCE["Erde"]["Sputnik 2"]))
        finally:
            DISTANCE = float(self.distance.text()) + CENTRAL_RADIUS + SAT_RADIUS ### so lassen?

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
            v0 = vp.vector(float(self.sat_v0_x.text()), float(self.sat_v0_y.text()), float(self.sat_v0_z.text()))

        if self.save_values.isChecked():
            with open("values.yml", "w+") as f:
                values = {
                "central_mass": CENTRAL_MASS,
                "central_radius": CENTRAL_RADIUS,
                "sat_mass": SAT_MASS,
                "sat_radius": SAT_RADIUS,
                "distance": DISTANCE - CENTRAL_RADIUS - SAT_RADIUS,
                "v0": {"x": v0.x, "y": v0.y, "z": v0.z}
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

    def load_values(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setText("Möchten Sie die gespeicherten Werte löschen oder behalten?")
        msg.setWindowTitle("gespeicherte Werte laden")
        msg.setStandardButtons(QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes)
        b_delete = msg.button(QtWidgets.QMessageBox.Yes)
        b_delete.setText("Löschen")
        b_save = msg.button(QtWidgets.QMessageBox.No)
        b_save.setText("Behalten")
        msg.setDefaultButton(b_save)
        msg.setEscapeButton(b_save)
        msg.exec()

        values = {}
        error = False
        if msg.clickedButton() == b_delete:
            try:
                with open("values.yml", "r") as f:
                    values = yaml.load(f, Loader=yaml.FullLoader)
                os.remove("values.yml")
            except FileNotFoundError:
                error = True
                err = QtWidgets.QMessageBox()
                err.setIcon(QtWidgets.QMessageBox.Critical)
                err.setText("keine gespeicherten Werte vorhanden")
                err.setWindowTitle("Fehler")
                err.exec()
        elif msg.clickedButton() == b_save:
            try:
                with open("values.yml", "r") as f:
                    values = yaml.load(f, Loader=yaml.FullLoader)
            except FileNotFoundError:
                error = True
                err = QtWidgets.QMessageBox()
                err.setIcon(QtWidgets.QMessageBox.Critical)
                err.setText("keine gespeicherten Werte vorhanden")
                err.setWindowTitle("Fehler")
                err.exec()

        if not error: # if the file could be loaded correctly
            try:
                self.central_mass.setText(str(values["central_mass"]))
                self.central_radius.setText(str(values["central_radius"]))
                self.sat_mass.setText(str(values["sat_mass"]))
                self.sat_radius.setText(str(values["sat_radius"]))
                self.distance.setText(str(values["distance"]))
                self.sat_v0_x.setText(str(values["v0"]["x"]))
                self.sat_v0_y.setText(str(values["v0"]["y"]))
                self.sat_v0_z.setText(str(values["v0"]["z"]))
            except TypeError:
                err = QtWidgets.QMessageBox()
                err.setIcon(QtWidgets.QMessageBox.Critical)
                err.setText("Werte-Datei fehlerhaft")
                err.setWindowTitle("Fehler")
                err.exec()

    def adjust_central_radius(self):
        """adjust radius of central"""
        central.radius = CENTRAL_RADIUS * central_radius_slider.value
        central_pointer.pos = central.pos - central_pointer.axis + vp.vector(0,central.radius,0)

    def reset_central_radius_slider(self):
        """reset the central radius slider"""
        central_radius_slider.value = 1
        self.adjust_central_radius()

    # def interrupt(self): # doesn't work
    #     t = t_max

    def open_vpython(self):
        """open vpython window with entered values"""
        self.read()
        # global t
        t = 0
        # global t_max
        t_max = self.settings.update_rate.value() * self.settings.max_seconds.value()
        testing = self.settings.do_testing.isChecked()
        scene = vp.canvas(title="Simulation zum Zweikörperproblem", height=self.settings.canvas_height.value(), width=self.settings.canvas_width.value())
        # initiate bodies itself
        global central
        central = vp.sphere(radius=CENTRAL_RADIUS, make_trail=True, color=vp.vector(self.settings.color_objects_r.value()/255, self.settings.color_objects_g.value()/255, self.settings.color_objects_b.value()/255))
        sat = vp.sphere(pos=vp.vector(DISTANCE,0,0), radius=SAT_RADIUS, make_trail=True, color=vp.vector(self.settings.color_objects_r.value()/255, self.settings.color_objects_g.value()/255, self.settings.color_objects_b.value()/255))

        # initiate pointers
        global central_pointer
        central_pointer = vp.arrow(axis=vp.vector(0,-(DISTANCE / 2),0), color=vp.vector(self.settings.color_pointer_r.value()/255, self.settings.color_pointer_g.value()/255, self.settings.color_pointer_b.value()/255)) # set pointer arrows to the objects because the scales are too large
        central_pointer.pos = central.pos - central_pointer.axis + vp.vector(0,CENTRAL_RADIUS,0) # set central pointer to the outside of central
        sat_pointer = vp.arrow(axis=vp.vector(0,-(DISTANCE / 5),0), color=vp.vector(self.settings.color_pointer_r.value()/255, self.settings.color_pointer_g.value()/255, self.settings.color_pointer_b.value()/255))

        # testing
        global central_radius_slider
        central_radius_slider = vp.slider(min=0.1, max=10, step=0.1, value=1, bind=self.adjust_central_radius)
        reset = vp.button(text="Reset", bind=self.reset_central_radius_slider)
        # close = vp.button(text="Close", bind=self.interrupt) # doesn't work

        if testing:
            pos1_s = sat.pos
            pos1_c = central.pos
            v_pos1_s = v0
            v_pos1_c = vp.vector(0,0,0)
        else:
            pos1 = sat.pos
            v_pos1 = v0
        while t < t_max: # movement
            vp.rate(self.settings.update_rate.value())
            if testing:
                G = scipy.constants.value(u"Newtonian constant of gravitation") # some values for calculations
                M = CENTRAL_MASS
                m = SAT_MASS
                r = central.pos - sat.pos # vector from sat to central

                # calculations: _s for sat, _c for central
                F_s = ((G * M * m) / (vp.mag(r) ** 2)) * vp.norm(r) # gravitational force
                F_c = ((G * M * m) / (vp.mag(r) ** 2)) * vp.norm(-r)
                a_s = F_s / m # gravitational acceleration
                a_c = F_c / M
                v_s = a_s * self.settings.t_factor.value() + v_pos1_s # velocity
                v_c = a_c * self.settings.t_factor.value() + v_pos1_c
                sat.pos = v_s * self.settings.t_factor.value() + pos1_s # new position
                central.pos = v_c * self.settings.t_factor.value() + pos1_c

                v_pos1_s = v_s # make the current velocity available for next iteration
                v_pos1_c = v_c
                pos1_s = sat.pos # make the current position available for next iteration
                pos1_c = central.pos
                sat_pointer.pos = sat.pos - sat_pointer.axis + vp.vector(0,SAT_RADIUS,0) # andere Möglichkeit ausprobieren (direkt bei sat definieren)
                central_pointer.pos = central.pos - central_pointer.axis + vp.vector(0,central.radius,0)
            else:
                G = scipy.constants.value(u"Newtonian constant of gravitation") # some values for calculations
                M = CENTRAL_MASS
                m = SAT_MASS
                r = central.pos - sat.pos # vector from sat to central

                # calculations
                F = ((G * M * m) / (vp.mag(r) ** 2)) * vp.norm(r) # gravitational force
                a = F / m # gravitational acceleration
                v = a * self.settings.t_factor.value() + v_pos1 # velocity
                sat.pos = v * self.settings.t_factor.value() + pos1 # new position

                v_pos1 = v # make the current velocity available for next iteration
                pos1 = sat.pos # make the current position available for next iteration
                sat_pointer.pos = sat.pos - sat_pointer.axis + vp.vector(0,SAT_RADIUS,0) # andere Möglichkeit ausprobieren (direkt bei sat definieren)
            t += 1
        if self.settings.do_restart.isChecked():
            self.restart()
