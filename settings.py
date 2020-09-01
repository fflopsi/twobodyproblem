import sys, data, re
from PyQt5 import uic, QtCore, QtGui, QtWidgets

class Settings(QtWidgets.QMainWindow):
    """window for settings"""
    def __init__(self, *args, parent = None, **kwargs):
        super(Settings, self).__init__(*args, parent, **kwargs)
        settings = uic.loadUi("ui/settings.ui", self)
        self.actionVerlassen.triggered.connect(self.close)
        self.b_cancel.clicked.connect(self.close)
        self.b_ok.clicked.connect(self.ok)
        self.b_save.clicked.connect(self.save) # "Übernehmen" button
        with open("SETTINGS.txt", "r") as f:
            cont = f.readlines()
            for x in range(len(cont)):
                if re.match(r"canvas_width", cont[x]):
                    self.canvas_width.setValue(int(cont[x + 1]))
                if re.match(r"canvas_height", cont[x]):
                    self.canvas_height.setValue(int(cont[x + 1]))
                if re.match(r"do_restart", cont[x]):
                    self.do_restart.setChecked(bool(int(cont[x + 1])))

    def save(self):
        cont = []
        with open("SETTINGS.txt", "r") as f:
            cont = f.readlines()
        with open("SETTINGS.txt", "w+") as f:
            for x in range(len(cont)):
                if re.match(r"canvas_width", cont[x]):
                    cont[x + 1] = str(self.canvas_width.value()) + "\n"
                if re.match(r"canvas_height", cont[x]):
                    cont[x + 1] = str(self.canvas_height.value()) + "\n"
                if re.match(r"do_restart", cont[x]):
                    if self.do_restart.isChecked():
                        cont[x + 1] = "1" + "\n"
                    else:
                        cont[x + 1] = "0" + "\n"
            f.write("".join(cont))

    def ok(self):
        self.save()
        self.close()
