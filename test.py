'''
Created on 23.06.2020
@author: flori
'''
import sys
import vpython as vp
from PySide2.QtWidgets import *

def execute(r):
    vp.box(size = vp.vector(0.5, 0.5, r), color = vp.color.red)

class widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.ok = QPushButton("ok")
        self.e = QLineEdit("123")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.ok)
        self.layout.addWidget(self.e)
        self.setLayout(self.layout)

        self.ok.clicked.connect(lambda: self.do(float(self.e.text())))

    def do(self, r):
        vp.box(size = vp.vector(0.5, 0.5, r), color = vp.color.red)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget1 = widget()
    widget1.show()
    sys.exit(app.exec_())
