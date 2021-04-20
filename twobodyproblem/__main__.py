import argparse
import os
import subprocess
import sys

import twobodyproblem
from twobodyproblem.options import Options
from twobodyproblem.values import Values
from twobodyproblem.visualization.simulation import Simulation

if __name__ == "__main__":
    # add CLI arguments
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
        version="%(prog)s version " + twobodyproblem.__version__,
        help="show the version of the program and exit"
    )
    parser.add_argument(
        "-d", "--debug", action="store_true",
        help="run the program with debug info prints"
    )
    parser.add_argument(
        "-n", "--nogui", action="store_true",
        help="run the program (the input section only) without the GUI, "
             "but with a CLI"
    )
    args = parser.parse_args()

    if args.debug:
        print("debugging activated...")
        print("passed arguments:", end=" ")
        print(sys.argv)
    if not args.nogui:
        inst_pkgs = [r.decode().split('==')[0] for r in
                     subprocess.check_output([sys.executable, '-m', 'pip',
                                              'freeze']).split()]
        if "PySide6" in inst_pkgs:
            # run the GUI app
            from PySide6 import QtWidgets
            from twobodyproblem.entry import EntryWindow
            app = QtWidgets.QApplication(sys.argv)
            window = EntryWindow(debug=args.debug)
            window.ui.show()
            sys.exit(app.exec_())
        else:
            # installation of PySide6 needed
            print("you need to install PySide6 to run this program in GUI "
                  "mode, so please do it with \"pip3 install PySide6\"")
            auto = input("input y/Y to install it automatically: ")
            if auto == "y" or auto == "Y":
                os.system("pip3 install PySide6 --upgrade")
                restart = input("input y/Y to relaunch the program: ")
                if restart == "y" or restart == "Y":
                    os.execl(sys.executable, "python", __file__, *sys.argv[1:])
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
        options = Options()
        try:
            options.canvas.width = int(input("canvas width (1000)[px]: "))
        except ValueError:
            pass
        try:
            options.canvas.height = int(input("canvas height (600)[px]: "))
        except ValueError:
            pass
        print("color objects RGB: ")
        try:
            options.colors.bodies.x = int(input("\tR (255): "))
        except ValueError:
            pass
        try:
            options.colors.bodies.y = int(input("\tG (255): "))
        except ValueError:
            pass
        try:
            options.colors.bodies.z = int(input("\tB (255): "))
        except ValueError:
            pass
        try:
            options.pointers = bool(int(input("show the pointers (1): ")))
        except ValueError:
            pass
        if options.pointers:
            print("color pointers RGB: ")
            try:
                options.colors.pointers.x = int(input("\tR (255): "))
            except ValueError:
                pass
            try:
                options.colors.pointers.y = int(input("\tG (0): "))
            except ValueError:
                pass
            try:
                options.colors.pointers.z = int(input("\tB (0): "))
            except ValueError:
                pass
        try:
            options.rate = int(input("calculations per second (100): "))
        except ValueError:
            pass
        try:
            options.sim_time = int(input("simulation length (30)[s]: "))
        except ValueError:
            pass
        try:
            options.delta_t = int(input("acceleration factor (Δt) (10): "))
        except ValueError:
            pass
        try:
            options.central_centered = bool(int(
                input("centered central body (0): ")))
        except ValueError:
            pass
        try:
            options.testing = bool(int(input("enable testing features (0): ")))
        except ValueError:
            pass
        try:
            options.restart = bool(int(
                input("restart the program after a simulation (1): ")))
        except ValueError:
            pass
        if args.debug:
            print("options:", end=" ")
            print(options.to_dict())

        print("\nNext, you need to input the values:")
        # default values
        values = Values()
        print("central body:")
        try:
            values.central.mass = float(input("\tmass (5.972e+24)[kg]: "))
        except ValueError:
            pass
        try:
            values.central.radius = float(input("\tradius (6371000)[m]: "))
        except ValueError:
            pass
        print("\tstarting velocity [m/s]:")
        try:
            values.central.velocity.x = float(input("\t\tspeed in x (0): "))
        except ValueError:
            pass
        try:
            values.central.velocity.y = float(input("\t\tspeed in y (0): "))
        except ValueError:
            pass
        try:
            values.central.velocity.z = float(input("\t\tspeed in z (0): "))
        except ValueError:
            pass
        print("satellite / second body:")
        try:
            values.sat.mass = float(input("\tmass (500)[kg]: "))
        except ValueError:
            pass
        try:
            values.sat.radius = float(input("\tradius (2)[m]: "))
        except ValueError:
            pass
        print("\tstarting velocity [m/s]:")
        try:
            values.sat.velocity.x = float(input("\t\tspeed in x (0): "))
        except ValueError:
            pass
        try:
            values.sat.velocity.y = float(input("\t\tspeed in y (0): "))
        except ValueError:
            pass
        try:
            values.sat.velocity.z = float(input("\t\tspeed in z (-8000): "))
        except ValueError:
            pass
        try:
            values.distance = float(input("\tinitial distance (1000000)[m]: "))
        except ValueError:
            pass
        if args.debug:
            print("values:", end=" ")
            print(values.to_dict())

        # create and start simulation
        Simulation(values=values, options=options).start()
