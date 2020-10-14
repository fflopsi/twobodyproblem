import sys, mainwindow
from PyQt5 import QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = mainwindow.MainWindow()
    window.show()

    sys.exit(app.exec())
