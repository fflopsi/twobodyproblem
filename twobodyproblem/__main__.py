import argparse
import sys

from PySide6 import QtWidgets

from twobodyproblem import entry
from twobodyproblem.visualization import simulation


def run(cli=False, debug=False):
    """runs the simulation

    args:
        cli: true if the program (value and option inputting) should be ran on
        the command line instead of a gui (default False)
        debug: true if the program should be run in debug mode (default False)
    """
    if debug:
        print("debugging activated ...")
        print("passed arguments:")
        print(sys.argv)
    if not cli:
        # run the GUI app
        # TODO: internationalization (English, German, ...)
        app = QtWidgets.QApplication(sys.argv)
        window = entry.MainWindow(debug=debug)
        window.ui.show()
        sys.exit(app.exec_())
    else:
        # run the CLI
        print("This is the command line interface for inputting the required "
              "options and values for the simulation.")
        print("If you leave something blank, the standard values in "
              "parentheses () will be used.")
        print("The unit is indicated in brackets [] if needed.")
        print("For the inputs that are yes/no, type 1 for yes and 0 for no.")
        print("\nFirst, you need to input the options:")
        # default options
        # TODO: options and values as classes
        options = {
            "canvas": {"width": 1000, "height": 600},
            "color": {
                "objects": {"r": 255, "g": 255, "b": 255},
                "pointer": {"r": 255, "g": 0, "b": 0},
            },
            "show_pointers": 1,
            "update_rate": 100,
            "max_seconds": 30,
            "t_factor": 10,
            "do_central_centered": 0,
            "do_testing": 0,
            "do_restart": 1
        }
        try:
            options["canvas"]["width"] = int(
                input("canvas width (1000)[px]: "))
        except ValueError:
            pass
        try:
            options["canvas"]["height"] = int(
                input("canvas height (600)[px]: "))
        except ValueError:
            pass
        print("color objects RGB: ")
        try:
            options["color"]["objects"]["r"] = int(
                input("\tR (255): "))
        except ValueError:
            pass
        try:
            options["color"]["objects"]["g"] = int(
                input("\tG (255): "))
        except ValueError:
            pass
        try:
            options["color"]["objects"]["b"] = int(
                input("\tB (255): "))
        except ValueError:
            pass
        try:
            options["show_pointers"] = int(
                input("show the pointers (1): "))
        except ValueError:
            pass
        if bool(options["show_pointers"]):
            print("color pointers RGB: ")
            try:
                options["color"]["pointer"]["r"] = int(
                    input("\tR (255): "))
            except ValueError:
                pass
            try:
                options["color"]["pointer"]["g"] = int(
                    input("\tG (0): "))
            except ValueError:
                pass
            try:
                options["color"]["pointer"]["b"] = int(
                    input("\tB (0): "))
            except ValueError:
                pass
        try:
            options["update_rate"] = int(
                input("calculations per second (100): "))
        except ValueError:
            pass
        try:
            options["max_seconds"] = int(
                input("simulation length (30)[s]: "))
        except ValueError:
            pass
        try:
            options["t_factor"] = int(
                input("acceleration factor (\u0394t) (10): "))
        except ValueError:
            pass
        try:
            options["do_central_centered"] = int(
                input("centered central body (0): "))
        except ValueError:
            pass
        try:
            options["do_testing"] = int(
                input("enable testing features (0): "))
        except ValueError:
            pass
        try:
            options["do_restart"] = int(
                input("restart the program after a simulation (1): "))
        except ValueError:
            pass
        if debug:
            print(options)

        print("\nNext, you need to input the values:")
        # default values
        values = {
            "central_mass": 5.972e+24,
            "central_radius": 6371000.0,
            "central_v0": {"x": 0.0, "y": 0.0, "z": 0.0},
            "sat_mass": 500.0,
            "sat_radius": 2.0,
            "sat_v0": {"x": 0.0, "y": 0.0, "z": -8000.0},
            "distance": 1000000.0
        }
        print("central body:")
        try:
            values["central_mass"] = float(input("\tmass (5.972e+24)[kg]: "))
        except ValueError:
            pass
        try:
            values["central_radius"] = float(input("\tradius (6371000)[m]: "))
        except ValueError:
            pass
        print("\tstarting velocity:")
        try:
            values["central_v0"]["x"] = float(
                input("\t\tspeed in x (0)[m/s]: "))
        except ValueError:
            pass
        try:
            values["central_v0"]["y"] = float(
                input("\t\tspeed in y (0)[m/s]: "))
        except ValueError:
            pass
        try:
            values["central_v0"]["z"] = float(
                input("\t\tspeed in z (0)[m/s]: "))
        except ValueError:
            pass
        print("satellite / second body:")
        try:
            values["sat_mass"] = float(input("\tmass (500)[kg]: "))
        except ValueError:
            pass
        try:
            values["sat_radius"] = float(input("\tradius (2)[m]: "))
        except ValueError:
            pass
        print("\tstarting velocity:")
        try:
            values["sat_v0"]["x"] = float(input("\t\tspeed in x (0)[m/s]: "))
        except ValueError:
            pass
        try:
            values["sat_v0"]["y"] = float(input("\t\tspeed in y (0)[m/s]: "))
        except ValueError:
            pass
        try:
            values["sat_v0"]["z"] = float(
                input("\t\tspeed in z (-8000)[m/s]: "))
        except ValueError:
            pass
        try:
            values["distance"] = float(
                input("\tstarting distance (1000000)[m]: "))
        except ValueError:
            pass
        if debug:
            print(values)

        # create and start simulation
        sim = simulation.Simulation(
            values=values, options=options)
        sim.start()


if __name__ == "__main__":
    # add CLI arguments
    # TODO: better documentation
    parser = argparse.ArgumentParser(
        prog="twobodyproblem",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage="python/python3 -m twobodyproblem [-h | -v | [-d] [-n]]",
        description="This is a little simulation of the gravitational two "
                    "body problem.\nTo use it normally in GUI mode, just run "
                    "the command without any of the optional arguments.",
        epilog="For further information, "
               "visit:\nhttps://github.com/flopsi-l-f/two-body"
               "-problem_simulation"
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
        help="run the program (the input section only) without the GUI, "
             "but with a CLI"
    )
    args = parser.parse_args()

    run(cli=args.nogui, debug=args.debug)
