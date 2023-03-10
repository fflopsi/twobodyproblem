import os
from pathlib import Path

import vpython as vp
import yaml

defaults = (1000, 600, 255, 255, 255, 1, 255, 0, 0, 100, 30, 10, 0, 0, 1)


class Options:
    """Contains all options used in the simulation
    
    Attributes:
    canvas: A Canvas object used for the vpython canvas
    colors: A Color object used for the colors of the bodies and pointers
    pointers: Show the pointers
    rate: The rate of calculations per second
    sim_time: Simulation time in seconds
    delta_t: Number of seconds calculated per calculation
    central_centered: Visually center the central body
    testing: Enable testing features
    restart: Restart the program after the simulation ends
    """

    class Canvas:
        """Represents vpython canvas
        
        Attributes:
        width: the width of the canvas in pixels
        height: the height of the canvas in pixels
        """

        def __init__(self, width=1000, height=600):
            """Initialize a Canvas with width and height"""
            self.width = width
            self.height = height

        @property
        def width(self):
            """Get and set width of the Canvas in pixels"""
            return self._width

        @width.setter
        def width(self, value):
            if not isinstance(value, int):
                raise TypeError("width must be an integer")
            if value < 100:
                raise ValueError("width must be greater than 100")
            self._width = value

        @property
        def height(self):
            """Get and set height of the Canvas in pixels"""
            return self._height

        @height.setter
        def height(self, value):
            if not isinstance(value, int):
                raise TypeError("height must be an integer")
            if value < 50:
                raise ValueError("height must be greater than 50")
            self._height = value

    class Color:
        """Stores color options for bodies and pointers
        
        Attributes:
        bodies: vector for the color values of the bodies (spheres)
        pointers: vector for the color values of the pointers (arrows)
        """

        def __init__(self, bodies_r=255, bodies_g=255, bodies_b=255,
                     pointers_r=255, pointers_g=0, pointers_b=0):
            """Initialize a Color class with RGB values for bodies and pointers"""
            self.bodies = vp.vector(bodies_r, bodies_g, bodies_b)
            self.pointers = vp.vector(pointers_r, pointers_g, pointers_b)

        @property
        def bodies(self):
            """Get and set bodies RGB color vector"""
            return self._bodies

        @bodies.setter
        def bodies(self, value):
            if not (0 <= value.x <= 255 and 0 <= value.y <= 255
                    and 0 <= value.z <= 255):
                raise ValueError("RGB values must be between 0 and 255")
            self._bodies = value

        @property
        def pointers(self):
            """Get and set pointers RGB color vector"""
            return self._pointers

        @pointers.setter
        def pointers(self, value):
            if not (0 <= value.x <= 255 and 0 <= value.y <= 255
                    and 0 <= value.z <= 255):
                raise ValueError("RGB values must be between 0 and 255")
            self._pointers = value

    def __init__(self, canvas_width=defaults[0], canvas_height=defaults[1],
                 color_objects_r=defaults[2], color_objects_g=defaults[3],
                 color_objects_b=defaults[4], show_pointers=defaults[5],
                 color_pointers_r=defaults[6], color_pointers_g=defaults[7],
                 color_pointers_b=defaults[8], update_rate=defaults[9],
                 max_seconds=defaults[10], delta_t=defaults[11],
                 central_centered=defaults[12], testing=defaults[13],
                 restart=defaults[14]):
        """Initialize an Options object with Canvas and Color objects split"""
        self.canvas = self.Canvas(width=canvas_width,
                                  height=canvas_height)
        self.colors = self.Color(bodies_r=color_objects_r,
                                 bodies_g=color_objects_g,
                                 bodies_b=color_objects_b,
                                 pointers_r=color_pointers_r,
                                 pointers_g=color_pointers_g,
                                 pointers_b=color_pointers_b)
        self.pointers = bool(show_pointers)
        self.rate = update_rate
        self.sim_time = max_seconds
        self.delta_t = delta_t
        self.central_centered = bool(central_centered)
        self.testing = bool(testing)
        self.restart = bool(restart)

    @classmethod
    def from_dict(cls, values: dict):
        """Create Options object from dictionary"""
        return cls(canvas_width=values["canvas"]["width"],
                   canvas_height=values["canvas"]["height"],
                   color_objects_r=values["color"]["objects"]["r"],
                   color_objects_g=values["color"]["objects"]["g"],
                   color_objects_b=values["color"]["objects"]["b"],
                   show_pointers=values["show_pointers"],
                   color_pointers_r=values["color"]["pointers"]["r"],
                   color_pointers_g=values["color"]["pointers"]["g"],
                   color_pointers_b=values["color"]["pointers"]["b"],
                   update_rate=values["update_rate"],
                   max_seconds=values["max_seconds"],
                   delta_t=values["t_factor"],
                   central_centered=values["do_central_centered"],
                   testing=values["do_testing"], restart=values["do_restart"])

    @classmethod
    def from_list(cls, values):
        """Create Options object from list or tuple"""
        return cls(canvas_width=values[0], canvas_height=values[1],
                   color_objects_r=values[2], color_objects_g=values[3],
                   color_objects_b=values[4], show_pointers=values[5],
                   color_pointers_r=values[6], color_pointers_g=values[7],
                   color_pointers_b=values[8], update_rate=values[9],
                   max_seconds=values[10], delta_t=values[11],
                   central_centered=values[12], testing=values[13],
                   restart=values[14])

    @classmethod
    def from_file(cls, path=None):
        """Create Options object from yaml file

        Arguments:
        path: path to file (default [user home dir]/Documents/
            TwoBodyProblem/default/settings.yml)
        """
        dir_path = str(Path.home()) + "/Documents/TwoBodyProblem/default"
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        if path is None:
            path = dir_path + "/settings.yml"
        with open(path, "r") as f:
            return cls.from_dict(yaml.load(f, Loader=yaml.FullLoader))

    @classmethod
    def from_input(cls):
        """Create Options object from user input"""
        options = list(defaults)
        try:
            options[0] = int(input("Canvas width (1000)[px]: "))
        except ValueError:
            pass
        try:
            options[1] = int(input("Canvas height (600)[px]: "))
        except ValueError:
            pass
        print("Color objects RGB: ")
        try:
            options[2] = int(input("\tR (255): "))
        except ValueError:
            pass
        try:
            options[3] = int(input("\tG (255): "))
        except ValueError:
            pass
        try:
            options[4] = int(input("\tB (255): "))
        except ValueError:
            pass
        try:
            options[5] = int(input("Show the pointers (1): "))
        except ValueError:
            pass
        if options[5] == 1:
            print("Color pointers RGB: ")
            try:
                options[6] = int(input("\tR (255): "))
            except ValueError:
                pass
            try:
                options[7] = int(input("\tG (0): "))
            except ValueError:
                pass
            try:
                options[8] = int(input("\tB (0): "))
            except ValueError:
                pass
        try:
            options[9] = int(input("Calculations per second (100): "))
        except ValueError:
            pass
        try:
            options[10] = int(input("Simulation length (30)[s]: "))
        except ValueError:
            pass
        try:
            options[11] = int(input("Acceleration factor (Δt) (10): "))
        except ValueError:
            pass
        try:
            options[12] = int(input("Centered central body (0): "))
        except ValueError:
            pass
        try:
            options[13] = int(input("Enable testing features (0): "))
        except ValueError:
            pass
        try:
            options[14] = int(input("Restart program after simulation (1): "))
        except ValueError:
            pass

        return cls.from_list(options)

    @property
    def rate(self):
        """Get and set update rate"""
        return self._rate

    @rate.setter
    def rate(self, value):
        if not isinstance(value, int):
            raise TypeError("rate must be an integer")
        if value < 1:
            raise ValueError("rate must be positive")
        self._rate = value

    @property
    def sim_time(self):
        """Get and set simulation time"""
        return self._sim_time

    @sim_time.setter
    def sim_time(self, value):
        if not isinstance(value, int):
            raise TypeError("sim_time must be an integer")
        if value < 0:
            raise ValueError("sim_time must be greater than 0 (zero)")
        self._sim_time = value

    @property
    def delta_t(self):
        """Get and set Δt"""
        return self._delta_t

    @delta_t.setter
    def delta_t(self, value):
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError("delta_t must be a number")
        if value <= 0:
            raise ValueError("delta_t must be positive")
        self._delta_t = value

    def to_dict(self) -> dict:
        """Convert the Options object to a dictionary"""
        return {
            "canvas": {
                "width": self.canvas.width,
                "height": self.canvas.height
            },
            "show_pointers": self.pointers,
            "color": {
                "objects": {
                    "r": self.colors.bodies.x,
                    "g": self.colors.bodies.y,
                    "b": self.colors.bodies.z
                },
                "pointers": {
                    "r": self.colors.pointers.x,
                    "g": self.colors.pointers.y,
                    "b": self.colors.pointers.z
                },
            },
            "update_rate": self.rate,
            "max_seconds": self.sim_time,
            "t_factor": self.delta_t,
            "do_central_centered": self.central_centered,
            "do_testing": self.testing,
            "do_restart": self.restart
        }

    def save(self, path=None):
        """Save content of Options to yaml file (overwriting existing content)

        Arguments:
        path: path to file (default [user home dir]/Documents/
            TwoBodyProblem/default/settings.yml)
        """
        dir_path = str(Path.home()) + "/Documents/TwoBodyProblem/default"
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        if path is None:
            path = dir_path + "/settings.yml"
        with open(path, "w+") as f:
            f.write(yaml.dump(self.to_dict()))
