# Two Body Problem
## a small simulation

**Welcome!**

This is my matriculation project. I wrote a small program to simulate the two body problem. You can either choose from the presets (like Sun, Earth, Moon etc.) or type in your own masses and volumes. The program will show you an approximation of the suitable conic section.

## Table of Contents

[Installation Instructions](#installation)  
- [Windows 10](#win10)  
- [Ubuntu, Debian and other Linux distros](#linux)  

<a name="installation"/>

## Installation Instructions

Read below for detailed instructions on how to use my program.

<a name="win10"/>

### Windows 10

- Python prerequisites:
  1. Download and install [Python 3.9](https://www.python.org/downloads/).
- Git and repository prerequisites:
  1. Download and install [Git Bash](https://gitforwindows.org/)
  2. Run the following commands from *git bash*:
      1. `mkdir Two\ Body\ Problem && cd "$_"`
      2. `git clone https://github.com/flopsi-l-f/two-body-problem_simulation.git`
  3. Run the following commands from the command line:
      1. `cd C:\Users\[Your Username]\Two Body Problem\two-body-problem_simulation`
      2. `pip install -r requirements.txt`

Now, the code is available and runnable with `python "C:\Users\[Your Username]\Two Body Problem\two-body-problem_simulation\run-main.py"`

(You may need Microsoft Visual C++ to run vpython, so install it from [here](https://visualstudio.microsoft.com/visual-cpp-build-tools/) if needed.)

<a name="linux"/>

### Ubuntu, Debian and other Linux distros

- Run the following commands in bash:
  - Not necessary, but recommended: `sudo apt-get update && sudo apt-get upgrade`
  1. `sudo apt-get install python3`
  2. `sudo apt-get install git`
  3. `mkdir Two\ Body\ Problem && cd "$_"`
  4. `git clone https://github.com/flopsi-l-f/two-body-problem_simulation.git`
  5. `cd two-body-problem_simulation`
  6. `pip3 install -r requirements.txt`

Now, the code is available and runnable with `python3 /home/[Your Username]/Two\ Body\ Problem/two-body-problem_simulation/run-main.py`

*Participation in this README is always welcome!*
