import sys, data
from PyQt5 import uic, QtCore, QtGui, QtWidgets

class Settings(QtWidgets.QMainWindow):
    """window for settings, no functionality yet"""
    def __init__(self, *args, parent = None, **kwargs):
        super(Settings, self).__init__(*args, parent, **kwargs)
        settings = uic.loadUi("settings.ui", self)
