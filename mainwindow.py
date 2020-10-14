import sys, data, examples, settings, os, math, scipy.constants
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
        self.actionListe_mit_Voreinstellungen.triggered.connect(self.examples.show)
        self.actionEinstellungen.triggered.connect(self.settings.show)

    def restart(self):
        """restart the program after simulation has finished"""
        os.execl(sys.executable, sys.executable, *sys.argv)

    def read(self):
        """make all the entered values globally accessible"""
        global central_mass
        global central_radius
        global sat_mass
        global sat_radius
        global distance
        global v0

        try:
            float(self.central_mass.text())
        except ValueError:
            self.central_mass.setText(str(data.MASS["Erde"]))
        finally:
            central_mass = float(self.central_mass.text())

        try:
            float(self.central_radius.text())
        except ValueError:
            self.central_radius.setText(str(data.RADIUS["Erde"]))
        finally:
            central_radius = float(self.central_radius.text())

        try:
            float(self.sat_mass.text())
        except ValueError:
            self.sat_mass.setText(str(data.MASS["Sputnik 2"]))
        finally:
            sat_mass = float(self.sat_mass.text())

        try:
            float(self.sat_radius.text())
        except ValueError:
            self.sat_radius.setText(str(data.RADIUS["Sputnik 2"]))
        finally:
            sat_radius = float(self.sat_radius.text())

        try:
            float(self.distance.text())
        except ValueError:
            self.distance.setText(str(data.DISTANCE["Erde"]["Sputnik 2"]))
        finally:
            distance = float(self.distance.text()) + central_radius + sat_radius ### so lassen?

        try:
            vp.vector(float(self.sat_v0_x.text()), float(self.sat_v0_y.text()), float(self.sat_v0_z.text()))
        except ValueError:
            self.sat_v0_x.setText("0")
            self.sat_v0_y.setText("0")
            self.sat_v0_z.setText("-8000")
        finally:
            v0 = vp.vector(float(self.sat_v0_x.text()), float(self.sat_v0_y.text()), float(self.sat_v0_z.text()))

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

    def adjust_central_radius(self):
        """adjust radius of central"""
        central.radius = central_radius * central_radius_slider.value
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
        scene = vp.canvas(title="Test", height=self.settings.canvas_height.value(), width=self.settings.canvas_width.value())
        # initiate bodies itself
        global central
        central = vp.sphere(radius=central_radius, color=vp.vector(self.settings.color_objects_r.value()/255, self.settings.color_objects_g.value()/255, self.settings.color_objects_b.value()/255))
        sat = vp.sphere(pos=vp.vector(distance,0,0), radius=sat_radius, make_trail=True, color=vp.vector(self.settings.color_objects_r.value()/255, self.settings.color_objects_g.value()/255, self.settings.color_objects_b.value()/255))

        # initiate pointers
        global central_pointer
        central_pointer = vp.arrow(axis=vp.vector(0,-(distance / 2),0), color=vp.vector(self.settings.color_pointer_r.value()/255, self.settings.color_pointer_g.value()/255, self.settings.color_pointer_b.value()/255)) # set pointer arrows to the objects because the scales are too large
        central_pointer.pos = central.pos - central_pointer.axis + vp.vector(0,central_radius,0) # set central pointer to the outside of central
        sat_pointer = vp.arrow(axis=vp.vector(0,-(distance / 5),0), color=vp.vector(self.settings.color_pointer_r.value()/255, self.settings.color_pointer_g.value()/255, self.settings.color_pointer_b.value()/255))

        # testing
        global central_radius_slider
        central_radius_slider = vp.slider(min=0.1, max=10, step=0.1, value=1, bind=self.adjust_central_radius)
        reset = vp.button(text="Reset", bind=self.reset_central_radius_slider)
        # close = vp.button(text="Close", bind=self.interrupt) # doesn't work

        pos1 = sat.pos
        v_pos1 = v0
        while t < t_max: # movement
            vp.rate(self.settings.update_rate.value())
            G = scipy.constants.value(u"Newtonian constant of gravitation") # some values for calculations
            M = central_mass
            m = sat_mass
            r = central.pos - sat.pos # vector from sat to central

            # calculations
            F = ((G * M * m) / (vp.mag(r) ** 2)) * vp.norm(r) # gravitational force
            a = F / m # gravitational acceleration
            v = a * self.settings.t_factor.value() + v_pos1 # velocity
            sat.pos = v * self.settings.t_factor.value() + pos1 # new position

            v_pos1 = v # make the current velocity available for next iteration
            pos1 = sat.pos # make the current position available for next iteration
            sat_pointer.pos = sat.pos - sat_pointer.axis + vp.vector(0,sat_radius,0) # andere Möglichkeit ausprobieren (direkt bei sat definieren)
            t += 1
        if self.settings.do_restart.isChecked():
            self.restart()
