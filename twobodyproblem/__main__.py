from twobodyproblem import entry
import argparse
import sys
from PySide6 import QtWidgets


def run(cli=False, debug=False):
    """runs the simulation"""
    if debug:
        print("debugging activated ...")
        print("passed arguments: " + sys.argv)
    if cli:
        print("This command line interface is not available yet. Please use the graphical user interface with the option \"gui\".")
    else:
        app = QtWidgets.QApplication(sys.argv)
        window = entry.MainWindow(debug=debug)
        window.ui.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="twobodyproblem",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage="python/python3 -m twobodyproblem [-h | -v | [-d] [-n]]",
        description="This is a little simulation of the gravitational two body problem.\nTo use it normally in GUI mode, just run the command without any of the optional arguments.",
        epilog="For further information, visit:\nhttps://github.com/flopsi-l-f/two-body-problem_simulation"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version="use \"pip3 show %(prog)s\"",
        help="show the version of the program and exit"
    )
    parser.add_argument(
        "-d", "--debug", action="store_true",
        help="run the program in debug mode"
    )
    parser.add_argument(
        "-n", "--nogui", action="store_true",
        help="run the program (the input section only) without the GUI, but with a CLI"
    )
    args = parser.parse_args()

    run(cli=args.nogui, debug=args.debug)
