from twobodyproblem import entry
import sys
from PySide6 import QtWidgets

if __name__ == "__main__":
    try:
        sys.argv[1]
        if sys.argv[1] == "debug":
            print(sys.argv)
    except:
        pass

    app = QtWidgets.QApplication(sys.argv)

    window = entry.MainWindow()
    window.ui.show()

    sys.exit(app.exec_())
