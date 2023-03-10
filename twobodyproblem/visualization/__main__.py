# this is deliberately kept short and simple, the main entry point for the
# program is the package twobodyproblem
# this package main file should only be used for developing and debugging
# purposes, as the inputs have to be complete or completely emtpy for the
# program in order to work

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
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        usage="python/python3 -m twobodyproblem.visualization [-h | -v ] "
              "-i values [-o options] [-d]",
        description="This is a little simulation of the gravitational two "
                    "body problem.\nTo use it normally in CLI mode, just run "
                    "the command without any of the optional arguments.",
        epilog="For further information, "
               "visit:\nhttps://github.com/twobodyproblem/simulation-python"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version="%(prog)s version " + twobodyproblem.__version__,
        help="Show the version of the program and exit"
    )
    parser.add_argument(
        "-d", "--debug", action="store_true",
        help="Run the program in debug mode"
    )
    parser.add_argument(
        "-i", "--input", nargs="*", default=[5.972e+24, 6371000.0, 0.0, 0.0,
                                             0.0, 500.0, 2.0, 0.0, 0.0,
                                             -8000.0, 1000000.0],
        help="Input the values in SI units in the following order: central "
             "mass, central radius, central velocity in x, y, z, satellite "
             "mass, satellite radius, satellite velocity in x, y, z, "
             "starting distance",
        metavar="values", type=float
    )
    parser.add_argument(
        "-o", "--options", nargs="*", default=[1000, 600, 255, 255, 255, 255,
                                               0, 0, 1, 100, 30, 10, 0, 0, 1],
        help="Input the options in the following order (1 for yes, 0 for no): "
             "canvas width, canvas height, color objects RGB, color pointers "
             "RGB, show pointers, calculations per second, simulation length "
             "in s, acceleration factor Δt, centered central body, testing "
             "features, restart after simulation",
        metavar="options", type=int
    )
    args = parser.parse_args()

    # convert inputs to usable objects
    try:
        args.input[10]
    except IndexError:
        raise ValueError("please provide more values")
    try:
        args.options[14]
    except IndexError:
        raise ValueError("please provide more options")
    values = Values.from_list(args.input)
    options = Options.from_list(args.options)

    if args.debug:
        print("Debugging activated...")
        print("Passed arguments:", end=" ")
        print(sys.argv)
        print("Values:", end=" ")
        print(values.to_dict())
        print("Options:", end=" ")
        print(options.to_dict())

    # create and start simulation
    Simulation(values=values, options=options).start()
