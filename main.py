import sys
import input
from PySide6 import QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = input.MainWindow()
    window.ui.show()

    sys.exit(app.exec_())
