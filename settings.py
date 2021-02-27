import yaml
from PySide6 import QtWidgets, QtUiTools, QtCore


class Settings(QtWidgets.QMainWindow):
    """window for settings"""

    def __init__(self, *args, parent=None, **kwargs):
        super(Settings, self).__init__(*args, parent, **kwargs)  # set up UI
        self.ui = QtUiTools.QUiLoader().load(QtCore.QFile("ui/settings.ui"))
        self.ui.actionVerlassen.triggered.connect(self.ui.close)
        self.ui.b_cancel.clicked.connect(self.ui.close)
        self.ui.b_ok.clicked.connect(lambda: (self.save(), self.ui.close()))
        self.ui.b_save.clicked.connect(self.save)
        self.ui.show_pointers.stateChanged.connect(
            self.show_pointers_changed_action)
        self.ui.do_central_unmoving.toggled.connect(
            self.central_changed_action)
        self.ui.tabWidget.setCurrentIndex(0)

        try:
            # set the different values to display in settings window
            with open("saved_data/settings.yml", "r") as f:
                conf = yaml.load(f, Loader=yaml.FullLoader)
                self.ui.canvas_width.setValue(conf["canvas"]["width"])
                self.ui.canvas_height.setValue(conf["canvas"]["height"])
                self.ui.do_restart.setChecked(bool(int(conf["do_restart"])))
                self.ui.do_testing.setChecked(bool(int(conf["do_testing"])))
                self.ui.do_central_unmoving.setChecked(
                    bool(int(conf["do_central_unmoving"])))
                self.ui.do_central_centered.setChecked(
                    bool(int(conf["do_central_centered"])))
                self.ui.color_objects_r.setValue(conf["color"]["objects"]["r"])
                self.ui.color_objects_g.setValue(conf["color"]["objects"]["g"])
                self.ui.color_objects_g.setValue(conf["color"]["objects"]["g"])
                self.ui.color_pointer_r.setValue(conf["color"]["pointer"]["r"])
                self.ui.color_pointer_g.setValue(conf["color"]["pointer"]["g"])
                self.ui.color_pointer_b.setValue(conf["color"]["pointer"]["b"])
                self.ui.show_pointers.setChecked(
                    bool(int(conf["show_pointers"])))
                self.ui.update_rate.setValue(conf["update_rate"])
                self.ui.max_seconds.setValue(conf["max_seconds"])
                self.ui.t_factor.setValue(conf["t_factor"])
        except FileNotFoundError:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Einstellungsdatei nicht gefunden")
            msg.setText("Es werden die Standard-Einstellungen angewendet.")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
            msg.exec()

        self.show_pointers_changed_action()
        self.central_changed_action()

    def save(self):
        """save the entered settings to a file"""
        with open("saved_data/settings.yml", "w+") as f:
            conf = {  # create the new settings content with the entered values
                "canvas": {
                    "width": self.ui.canvas_width.value(),
                    "height": self.ui.canvas_height.value()
                },
                "do_restart": int(self.ui.do_restart.isChecked()),
                "do_testing": int(self.ui.do_testing.isChecked()),
                "do_central_unmoving": int(self.ui.do_central_unmoving.isChecked()),
                "do_central_centered": int(self.ui.do_central_centered.isChecked()),
                "color": {
                    "objects": {
                        "r": self.ui.color_objects_r.value(),
                        "g": self.ui.color_objects_g.value(),
                        "b": self.ui.color_objects_b.value()
                    },
                    "pointer": {
                        "r": self.ui.color_pointer_r.value(),
                        "g": self.ui.color_pointer_g.value(),
                        "b": self.ui.color_pointer_b.value()
                    }
                },
                "show_pointers": int(self.ui.show_pointers.isChecked()),
                "update_rate": self.ui.update_rate.value(),
                "max_seconds": self.ui.max_seconds.value(),
                "t_factor": self.ui.t_factor.value(),
            }
            f.write(yaml.dump(conf))

    def show_pointers_changed_action(self):
        if self.ui.show_pointers.isChecked():
            self.ui.color_pointer_r.setEnabled(True)
            self.ui.color_pointer_g.setEnabled(True)
            self.ui.color_pointer_b.setEnabled(True)
        else:
            self.ui.color_pointer_r.setEnabled(False)
            self.ui.color_pointer_g.setEnabled(False)
            self.ui.color_pointer_b.setEnabled(False)

    def central_changed_action(self):
        if self.ui.do_central_unmoving.isChecked():
            self.parent().ui.central_v0_x.setEnabled(False)
            self.parent().ui.central_v0_y.setEnabled(False)
            self.parent().ui.central_v0_z.setEnabled(False)
        else:
            self.parent().ui.central_v0_x.setEnabled(True)
            self.parent().ui.central_v0_y.setEnabled(True)
            self.parent().ui.central_v0_z.setEnabled(True)
