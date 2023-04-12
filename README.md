# Two Body Problem

### a small simulation

**Welcome!**

I wrote a small program in Python to simulate the two body problem. You type in
some parameters, like mass, radius, velocity and distance. The program will
show you a visualization of the simulation.

*This program is command line only. If you want a graphical user interface for
inputting your data,
visit [this repository](https://github.com/fflopsi/twobodyproblem-gui)
containing a GUI program.*

## Installation

*(You may need Microsoft Visual C++ to be able to run the program, so install
it from [here](https://visualstudio.microsoft.com/visual-cpp-build-tools) if
needed.)*

### Via PyPi

*The Python package manager pip will install the last uploaded version from the
Python Package Index [PyPi](https://pypi.org/project/twobodyproblem). This will
not always be the latest version, so if you want to install all the latest
features, install it from GitHub (see [below](#via-github)).*

1. Make sure [Python](https://www.python.org/downloads) and pip are installed
   correctly.
1. Run these commands from a command line:
    1. `pip install --upgrade pip setuptools wheel`
    1. `pip install --upgrade twobodyproblem`
1. Now, the program is usable with `python -m twobodyproblem`.

### Via GitHub

1. Make sure [Python](https://www.python.org/downloads) and pip are installed
   correctly.
1. Make sure [Git SCM](https://git-scm.com/downloads) is installed correctly.
1. Run these commands from a command line:
    1. `mkdir TwoBody` and `cd TwoBody`
    1. `git clone https://github.com/fflopsi/twobodyproblem.git`
    1. `pip install --upgrade pip setuptools wheel`
    1. `pip install ./twobodyproblem/`
1. Now, the program is usable with `python -m twobodyproblem`.

## Usage

*To learn more about how to run the program with different options,
run `python -m twbodyproblem -h`.*

Run the program with `python -m twobodyproblem` on a command line.

First, you will have to input *options* and *values*. The options define the
particular behavior of the simulation, the values define the dimensions (i.e.
mass, radius, distance, velocity) of the bodies. You can either load them from
a prepared [YAML](https://yaml.org) file (*.yml) or type them in directly.
After having them typed in, you can choose to save them in a file for later
use. When saving to an existing file, the previous contents of the file will
be **overwritten**. When working with these files, you need to have the exact
paths to the files at hand. Otherwise, the default files for saving/loading
will be used.

The simulation window will open automatically after the last input.

During the simulation, you are able to pause, un-pause and stop the simulation
with the accordingly named buttons below the black rectangle. The restart
button restarts the *whole* program, not just the simulation.

The sliders below the buttons can be used to magnify the bodies in the
simulation. This magnification does not affect the physics, it is only a visual
help.
