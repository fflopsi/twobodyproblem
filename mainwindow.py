import sys, data, examples, settings, os
import vpython as vp
from PyQt5 import uic, QtCore, QtGui, QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    """the main window, or entry window"""
    def __init__(self, *args, parent = None, **kwargs):
        super(MainWindow, self).__init__(*args, parent, **kwargs)
        uic.loadUi("ui/entry.ui", self)
        self.setWindowIcon(QtGui.QIcon("ui/icon.gif"))
        self.examples = examples.Examples(parent = self)
        self.settings = settings.Settings(parent = self)
        self.actionVerlassen.triggered.connect(self.close)
        self.b_ok.clicked.connect(self.open_vpython)
        self.b_reset.clicked.connect(self.clear_fields)
        self.actionListe_mit_Voreinstellungen.triggered.connect(self.examples.show)
        self.actionEinstellungen.triggered.connect(self.settings.show)
        global central_mass_default

    def restart(self):
        os.execl(sys.executable, sys.executable, *sys.argv)

    def read(self):
        """make all the entered values globally accessible"""
        global central_mass
        global central_radius
        global sat_mass
        global sat_radius
        global distance
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
            distance = float(self.distance.text()) + central_radius + sat_radius

    def clear_fields(self):
        """delete all values in all fields"""
        self.central_radius.setText("")
        self.central_mass.setText("")
        self.sat_mass.setText("")
        self.sat_radius.setText("")
        self.distance.setText("")

    def open_vpython(self):
        """open vpython window with entered values"""
        self.read()
        scene = vp.canvas(title = "Test", height = int(self.settings.canvas_height.value()), width = int(self.settings.canvas_width.value()))
        central = vp.sphere(radius = central_radius, color = vp.vector(int(self.settings.color_objects_r.value())/255, int(self.settings.color_objects_g.value())/255, int(self.settings.color_objects_b.value())/255))
        sat = vp.sphere(pos = vp.vector(distance,0,0), radius = sat_radius, make_trail = True, color = vp.vector(int(self.settings.color_objects_r.value())/255, int(self.settings.color_objects_g.value())/255, int(self.settings.color_objects_b.value())/255))
        central_pointer = vp.arrow(axis = vp.vector(0,-(distance / 5),0), color = vp.vector(int(self.settings.color_pointer_r.value())/255, int(self.settings.color_pointer_g.value())/255, int(self.settings.color_pointer_b.value())/255)) # set pointer arrows to the objects because the scales are too large
        central_pointer.pos = central.pos - central_pointer.axis + vp.vector(0,central_radius,0) # set central pointer to the outside of central
        sat_pointer = vp.arrow(axis = vp.vector(0,-(distance / 5),0), color = vp.vector(int(self.settings.color_pointer_r.value())/255, int(self.settings.color_pointer_g.value())/255, int(self.settings.color_pointer_b.value())/255))
        x = 0
        while x < 300: # simple movement
            vp.rate(30)
            sat.pos += vp.vector(distance,0,0) / 300
            sat_pointer.pos = sat.pos - sat_pointer.axis + vp.vector(0,sat_radius,0)
            x += 1
        if self.settings.do_restart.isChecked():
            self.restart()
