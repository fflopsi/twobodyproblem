import sys
import input
from PyQt5 import QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = input.MainWindow()
    window.show()

    sys.exit(app.exec())
