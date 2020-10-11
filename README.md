# Two Body Problem
## a small simulation

**Welcome!**

This is my matriculation project. I wrote a small program to simulate the two body problem. You can either choose from the presets (like the Sun, the Earth, Moon etc.) or type in your own masses and volumes. ATM, the only orbit available is a (perfect) circle.

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
  1. Download and install [Python 3.8](https://www.python.org/downloads/).
  2. Run the following commands from the command line to install required packages:
    - `pip install pyqt5`
    - `pip install vpython`
    - `pip install scipy`
- Git and repository prerequisites:
  1. Download and install [Git Bash](https://gitforwindows.org/)
  2. Run the following commands from *git bash*:
    1. `mkdir Two\ Body\ Problem && cd "$_"`
    2. `git clone https://github.com/flopsi-l-f/two-body-problem_simulation.git`

Now, the code is available and runnable with `python "C:\Users\[Your Username]\Two Body Problem\two-body-problem_simulation\run-main.py"`

<a name="linux"/>

## Ubuntu, Debian and other Linux distros

- Run the following commands in bash
  0. not necessary, but recommended: `sudo apt-get update && sudo apt-get upgrade`
  1. `sudo apt-get install python3`
  2. Install the required python packages:
    - `pip install pyqt5`
    - `pip install vpython`
    - `pip install scipy`
  3. `sudo apt-get install git`
  4. `mkdir Two\ Body\ Problem && cd "$_"`
  5. `git clone https://github.com/flopsi-l-f/two-body-problem_simulation.git`

Now, the code is available and runnable with `python3 /home/[Your Username]/Two\ Body\ Problem/two-body-problem_simulation/run-main.py`
