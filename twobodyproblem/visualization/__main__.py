# this is deliberately kept short and simple, the main entry point for the
# program is the package twobodyproblem
# this package main file should only be used for developing and debugging
# purposes, as the inputs have to be complete or completely emtpy for the
# program in order to work

import argparse
import sys

from twobodyproblem.visualization import simulation

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
        "-i", "--input", nargs="*", default=[5.972e+24, 6371000.0, 0.0, 0.0,
                                             0.0, 500.0, 2.0, 0.0, 0.0,
                                             -8000.0, 1000000.0],
        help="input the values in SI units in the following order: central "
             "mass, central radius, central velocity in x, y, z, satellite "
             "mass, satellite radius, satellite velocity in x, y, z, "
             "starting distance",
        metavar="values", type=float
    )
    parser.add_argument(
        "-o", "--options", nargs="*", default=[1000, 600, 255, 255, 255, 255,
                                               0, 0, 1, 100, 30, 10, 0, 0,
                                               1],
        help="input the options in the following order (1 for yes, 0 for no): "
             "canvas width, canvas height, color objects RGB, color pointers "
             "RGB, show pointers, calculations per second, simulation length "
             "in s, acceleration factor Δt, centered central body, testing "
             "features, restart after simulation",
        metavar="options", type=int
    )
    args = parser.parse_args()

    # convert inputs to dictionaries
    try:
        values = {
            "central_mass": args.input[0],
            "central_radius": args.input[1],
            "central_v0": {"x": args.input[2], "y": args.input[3],
                           "z": args.input[4]},
            "sat_mass": args.input[5],
            "sat_radius": args.input[6],
            "sat_v0": {"x": args.input[7], "y": args.input[8],
                       "z": args.input[9]},
            "distance": args.input[10]
        }
    except IndexError:
        raise ValueError("please provide more values")
    try:
        options = {
            "canvas": {"width": args.options[0], "height": args.options[1]},
            "color": {
                "objects": {"r": args.options[2], "g": args.options[3],
                            "b": args.options[4]},
                "pointer": {"r": args.options[5], "g": args.options[6],
                            "b": args.options[7]},
            },
            "show_pointers": args.options[8],
            "update_rate": args.options[9],
            "max_seconds": args.options[10],
            "t_factor": args.options[11],
            "do_central_centered": args.options[12],
            "do_testing": args.options[13],
            "do_restart": args.options[14]
        }
    except IndexError:
        raise ValueError("please provide more options")

    if args.debug:
        print("debugging activated ...")
        print("passed arguments:", end=" ")
        print(sys.argv)
        print("options:", end=" ")
        print(options)
        print("values:", end=" ")
        print(values)

    # create and start simulation
    sim = simulation.Simulation(values=values, options=options)
    sim.start()
