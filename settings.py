import yaml
from PyQt5 import uic, QtWidgets


class Settings(QtWidgets.QMainWindow):
    """window for settings"""

    def __init__(self, *args, parent=None, **kwargs):
        super(Settings, self).__init__(*args, parent, **kwargs)  # set up UI
        uic.loadUi("ui/settings.ui", self)
        self.actionVerlassen.triggered.connect(self.close)
        self.b_cancel.clicked.connect(self.close)
        self.b_ok.clicked.connect(lambda: (self.save(), self.close()))
        self.b_save.clicked.connect(self.save)
        self.show_pointers.stateChanged.connect(
            self.show_pointers_changed_action)
        self.do_central_unmoving.toggled.connect(
            self.central_changed_action)

        try:
            # set the different values to display in settings window
            with open("saved_data/settings.yml", "r") as f:
                conf = yaml.load(f, Loader=yaml.FullLoader)
                self.canvas_width.setValue(conf["canvas"]["width"])
                self.canvas_height.setValue(conf["canvas"]["height"])
                self.do_restart.setChecked(bool(int(conf["do_restart"])))
                self.do_testing.setChecked(bool(int(conf["do_testing"])))
                self.do_central_unmoving.setChecked(
                    bool(int(conf["do_central_unmoving"])))
                self.do_central_centered.setChecked(
                    bool(int(conf["do_central_centered"])))
                self.color_objects_r.setValue(conf["color"]["objects"]["r"])
                self.color_objects_g.setValue(conf["color"]["objects"]["g"])
                self.color_objects_g.setValue(conf["color"]["objects"]["g"])
                self.color_pointer_r.setValue(conf["color"]["pointer"]["r"])
                self.color_pointer_g.setValue(conf["color"]["pointer"]["g"])
                self.color_pointer_b.setValue(conf["color"]["pointer"]["b"])
                self.show_pointers.setChecked(bool(int(conf["show_pointers"])))
                self.update_rate.setValue(conf["update_rate"])
                self.max_seconds.setValue(conf["max_seconds"])
                self.t_factor.setValue(conf["t_factor"])
        except FileNotFoundError:
            pass

        self.show_pointers_changed_action()
        self.central_changed_action()

    def save(self):
        """save the entered settings to a file"""
        with open("saved_data/settings.yml", "w+") as f:
            conf = {  # create the new settings content with the entered values
                "canvas": {
                    "width": self.canvas_width.value(),
                    "height": self.canvas_height.value()
                },
                "do_restart": int(self.do_restart.isChecked()),
                "do_testing": int(self.do_testing.isChecked()),
                "do_central_unmoving": int(self.do_central_unmoving.isChecked()),
                "do_central_centered": int(self.do_central_centered.isChecked()),
                "color": {
                    "objects": {
                        "r": self.color_objects_r.value(),
                        "g": self.color_objects_g.value(),
                        "b": self.color_objects_b.value()
                    },
                    "pointer": {
                        "r": self.color_pointer_r.value(),
                        "g": self.color_pointer_g.value(),
                        "b": self.color_pointer_b.value()
                    }
                },
                "show_pointers": int(self.show_pointers.isChecked()),
                "update_rate": self.update_rate.value(),
                "max_seconds": self.max_seconds.value(),
                "t_factor": self.t_factor.value()
            }
            f.write(yaml.dump(conf))

    def show_pointers_changed_action(self):
        if self.show_pointers.isChecked():
            self.color_pointer_r.setEnabled(True)
            self.color_pointer_g.setEnabled(True)
            self.color_pointer_b.setEnabled(True)
        else:
            self.color_pointer_r.setEnabled(False)
            self.color_pointer_g.setEnabled(False)
            self.color_pointer_b.setEnabled(False)

    def central_changed_action(self):
        if self.do_central_unmoving.isChecked():
            self.parent().central_v0_x.setEnabled(False)
            self.parent().central_v0_y.setEnabled(False)
            self.parent().central_v0_z.setEnabled(False)
        else:
            self.parent().central_v0_x.setEnabled(True)
            self.parent().central_v0_y.setEnabled(True)
            self.parent().central_v0_z.setEnabled(True)
