# Two Body Problem

### a small simulation

**Welcome!**

I wrote a small program to simulate the two body problem.
You can either choose from presets (like Sun, Earth, Moon etc.)
or type in your own masses and volumes.
The program will show you a visualization of the simulation.

## Table of Contents

[Installation Instructions](#installation-instructions)  
- [via PyPi](#via-pypi)  
- [via GitHub](#via-github)  

[Usage](#usage)
  
## Installation Instructions

### via PyPi

*The Python package manager pip will install the last uploaded version
from the Python Package Index [PyPi](https://pypi.org/project/twobodyproblem).
This will not always be the latest version, so if you want to install all the latest features,
install it from git (see [below](#via-github)).*

1. Make sure [Python](https://www.python.org/downloads) and pip are installed correctly.
1. Run `pip3 install --upgrade pip setuptools wheel twobodyproblem` from a command line.
1. Now, the program is runnable with `python -m twobodyproblem` or `python3 -m twobodyproblem`.

(You may need Microsoft Visual C++ to be able to run the program,
so install it from [here](https://visualstudio.microsoft.com/visual-cpp-build-tools) if needed.)

### via GitHub

1. Make sure [Python](https://www.python.org/downloads) and pip are installed correctly.
1. Make sure [Git SCM](https://git-scm.com/downloads) is installed correctly.
1. Run these commands from a command line:
    1. `mkdir TwoBody` and `cd TwoBody`
    1. `git clone https://github.com/Two-Body-Problem/simulation-python.git`
    1. `pip3 install --upgrade pip setuptools wheel`
    1. `pip3 install two-body-problem_simulation`
1. Now, the program is runnable with `python -m twobodyproblem` or `python3 -m twobodyproblem`.
    
(You may need Microsoft Visual C++ to be able to run the program,
so install it from [here](https://visualstudio.microsoft.com/visual-cpp-build-tools) if needed.)

## Usage

*To learn more about how to run the program with different options,
run `python -m twbodyproblem -h` or `python3 -m twbodyproblem -h` respectively.*

The program (better: the inputting section) can be run either
with a graphical user interface (GUI) or with a command line interface (CLI).

No matter if you run the program in GUI or CLI mode, you will have to input *options* and *values*.
The options define the particular behavior of the simulation,
the values define the dimensions (i.e. mass, radius, distance, velocity) of the bodies.

Saving options and values is currently only supported in GUI mode.
The options are automatically saved if you press one of the two buttons
in the lower right corner of the settings window (open it with <kbd>Ctrl</kbd>+<kbd>I</kbd>).
To save values, press <kbd>Ctrl</kbd>+<kbd>S</kbd>. The values will then be saved into a file.
If you do this action repeatedly, the former contents of the file (i.e. the saved values) will be **overwritten**!
To load saved values from this file, press <kbd>Ctrl</kbd>+<kbd>L</kbd>.
To save or load values through a file dialog,
press <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>S</kbd> or <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>L</kbd>.
These files will be saved in the [YAML](https://yaml.org) format (*.yml).

In GUI mode, you can select from a few presets (e.g. Sun, Moon, Earth) to fill in some values.
To do so, press <kbd>Ctrl</kbd>+<kbd>E</kbd>, select from the drop-down menu
and press one of the two buttons in the lower right corner.

In CLI mode, the simulation will start automatically after the last input.
To start the simulation from GUI mode, press the button in the lower right corner.

During the simulation, you are able to pause, un-pause and stop the simulation
with the accordingly named buttons below the black rectangle.
The restart button restarts the *whole* program, not just the simulation.

The sliders below the buttons can be used to magnify the bodies in the simulation.
This magnification does not affect the physics, it is only a visual help.

***

*Participation in this README is always welcome!*
