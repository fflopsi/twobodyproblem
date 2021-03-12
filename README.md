# Two Body Problem
### a small simulation

**Welcome!**

I wrote a small program to simulate the two body problem. You can either choose from presets (like Sun, Earth, Moon etc.) or type in your own masses and volumes. The program will show you a visualization of the simulation.

## Table of Contents

[Installation Instructions](#installation)  
- [Windows 10](#win10)  
- [Ubuntu, Debian and other Linux distros](#linux)  

<a name="installation"/>

## Installation Instructions

Read below for detailed instructions on how to install my program.

<a name="win10"/>

### Windows 10

- Python prerequisites:
  1. Download and install [Python 3.9](https://www.python.org/downloads/).
- Git and repository prerequisites:
  1. Download and install [Git SCM](https://gitforwindows.org/)
  2. Run the following commands from *git bash*:
      1. `mkdir Two\ Body\ Problem && cd "$_"`
      2. `git clone https://github.com/flopsi-l-f/two-body-problem_simulation.git`
  3. Run the following command from the command line:
      1. `cd C:\Users\[Your Username]\Two Body Problem\two-body-problem_simulation`
      2. `pip install .`

Now, the code is available and runnable with `python -m twobodyproblem`

(You may need Microsoft Visual C++ to run vpython, so install it from [here](https://visualstudio.microsoft.com/visual-cpp-build-tools/) if needed.)

<a name="linux"/>

### Ubuntu, Debian and other Linux distros

- Run the following commands in bash:
  - Not necessary, but recommended: `sudo apt-get update && sudo apt-get upgrade`
  1. `sudo apt-get install python3`
  2. `sudo apt-get install git`
  3. `sudo apt-get install libopengl0`
  4. `mkdir Two\ Body\ Problem && cd "$_"`
  5. `git clone https://github.com/flopsi-l-f/two-body-problem_simulation.git`
  6. `cd two-body-problem_simulation`
  7. `pip3 install .`

Now, the code is available and runnable with `python3 -m twobodyproblem`

*Participation in this README is always welcome!*
