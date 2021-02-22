import sys
import input
from PyQt5 import QtWidgets

if __name__ == "__main__":
    currentExitCode = input.MainWindow.EXIT_CODE_REBOOT
    while currentExitCode == input.MainWindow.EXIT_CODE_REBOOT:
        app = QtWidgets.QApplication(sys.argv)

        window = input.MainWindow()
        window.show()

        currentExitCode = app.exec()
        # sys.exit(app.exec())
        app = None
