import sys, data, re
from PyQt5 import uic, QtCore, QtGui, QtWidgets

class Settings(QtWidgets.QMainWindow):
    """window for settings"""
    def __init__(self, *args, parent=None, **kwargs):
        super(Settings, self).__init__(*args, parent, **kwargs)
        settings = uic.loadUi("ui/settings.ui", self)
        self.actionVerlassen.triggered.connect(self.close)
        self.b_cancel.clicked.connect(self.close)
        self.b_ok.clicked.connect(self.ok)
        self.b_save.clicked.connect(self.save) # "Übernehmen" button
        try:
            with open("SETTINGS.txt", "r") as f:
                cont = f.readlines()
                for x in range(len(cont)):
                    if re.match(r"canvas_width", cont[x]):
                        self.canvas_width.setValue(int(cont[x+1]))
                    if re.match(r"canvas_height", cont[x]):
                        self.canvas_height.setValue(int(cont[x+1]))
                    if re.match(r"do_restart", cont[x]):
                        self.do_restart.setChecked(bool(int(cont[x+1])))
                    if re.match(r"color_objects_r", cont[x]):
                        self.color_objects_r.setValue(int(cont[x+1]))
                    if re.match(r"color_objects_g", cont[x]):
                        self.color_objects_g.setValue(int(cont[x+1]))
                    if re.match(r"color_objects_b", cont[x]):
                        self.color_objects_b.setValue(int(cont[x+1]))
                    if re.match(r"color_pointer_r", cont[x]):
                        self.color_pointer_r.setValue(int(cont[x+1]))
                    if re.match(r"color_pointer_g", cont[x]):
                        self.color_pointer_g.setValue(int(cont[x+1]))
                    if re.match(r"color_pointer_b", cont[x]):
                        self.color_pointer_b.setValue(int(cont[x+1]))
        except FileNotFoundError:
            with open("SETTINGS.txt", "w+") as f:
                f.write("")

    def blank(self, list, length):
        list = [None] * length
        list[0] = "canvas_width\n"
        list[2] = "canvas_height\n"
        list[4] = "do_restart\n"
        list[6] = "color_objects_r\n"
        list[8] = "color_objects_g\n"
        list[10] = "color_objects_b\n"
        list[12] = "color_pointer_r\n"
        list[14] = "color_pointer_g\n"
        list[16] = "color_pointer_b\n"
        return list

    def save(self):
        cont = []
        with open("SETTINGS.txt", "r") as f:
            cont = f.readlines()
        if cont == []:
            cont = self.blank(cont, 18)
        with open("SETTINGS.txt", "w+") as f:
            for x in range(len(cont)):
                if re.match(r"canvas_width", cont[x]):
                    cont[x+1] = str(self.canvas_width.value()) + "\n"
                if re.match(r"canvas_height", cont[x]):
                    cont[x+1] = str(self.canvas_height.value()) + "\n"
                if re.match(r"do_restart", cont[x]):
                    if self.do_restart.isChecked():
                        cont[x+1] = "1" + "\n"
                    else:
                        cont[x+1] = "0" + "\n"
                if re.match(r"color_objects_r", cont[x]):
                    cont[x+1] = str(self.color_objects_r.value()) + "\n"
                if re.match(r"color_objects_g", cont[x]):
                    cont[x+1] = str(self.color_objects_g.value()) + "\n"
                if re.match(r"color_objects_b", cont[x]):
                    cont[x+1] = str(self.color_objects_b.value()) + "\n"
                if re.match(r"color_pointer_r", cont[x]):
                    cont[x+1] = str(self.color_pointer_r.value()) + "\n"
                if re.match(r"color_pointer_g", cont[x]):
                    cont[x+1] = str(self.color_pointer_g.value()) + "\n"
                if re.match(r"color_pointer_b", cont[x]):
                    cont[x+1] = str(self.color_pointer_b.value()) + "\n"
            f.write("".join(cont))

    def ok(self):
        self.save()
        self.close()
