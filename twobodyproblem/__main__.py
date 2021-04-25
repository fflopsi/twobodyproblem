import argparse
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
        usage="python/python3 -m twobodyproblem [-h | -v ] [-d]",
        description="This is a little simulation of the gravitational two "
                    "body problem.\nTo run the simulation normally, just run "
                    "the command without any of the optional arguments.",
        epilog="For further information, "
               "visit:\nhttps://github.com/Two-Body-Problem/twobodyproblem"
               "-simulation-python"
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
    args = parser.parse_args()

    if args.debug:
        print("debugging activated...")
        print("passed arguments:", end=" ")
        print(sys.argv)

    # run the CLI
    print("\nThis is the command line interface for inputting the required "
          "options and values for the simulation.")
    print("If you leave something blank, the standard values in "
          "parentheses () will be used.")
    print("The unit is indicated in brackets [] if needed.")
    print("For the inputs that are yes/no, type 1 for yes and 0 for no.")

    open_val = input("\nIf you want to import values from a file, type y/Y: ")
    if open_val == "y" or open_val == "Y":
        path = input("Input the path to the file (if left empty, "
                     "the standard file will be used): ")
        if path == "":
            values = Values.from_file()
        else:
            values = Values.from_file(path)
    else:
        print("\nFirst, you need to input the values:")
        values = Values.from_input()
        save_val = input("\nIf you want to save these values to a file, "
                         "type y/Y: ")
        if save_val == "y" or save_val == "Y":
            path = input("Input the path to the file (if left empty, "
                         "the standard file will be used): ")
            if path == "":
                values.save()
            else:
                values.save(path)
    if args.debug:
        print("values:", end=" ")
        print(values.to_dict())

    open_opt = input("\nIf you want to import options from a file, type y/Y: ")
    if open_opt == "y" or open_opt == "Y":
        path = input("Input the path to the file (if left empty, "
                     "the standard file will be used): ")
        if path == "":
            options = Options.from_file()
        else:
            options = Options.from_file(path)
    else:
        print("\nNext, you need to input the options:")
        options = Options.from_input()
        save_opt = input("\nIf you want to save these options to a file, "
                         "type y/Y: ")
        if save_opt == "y" or save_opt == "Y":
            path = input("Input the path to the file (if left empty, "
                         "the standard file will be used): ")
            if path == "":
                options = Options.from_file()
            else:
                options = Options.from_file(path)
    if args.debug:
        print("options:", end=" ")
        print(options.to_dict())

    # create and start simulation
    Simulation(values=values, options=options).start()
