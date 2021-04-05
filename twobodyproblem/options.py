import vpython as vp


class OptionsCanvas:
    """class used for representing vpython canvases in Options"""

    def __init__(self, width=1000, height=600):
        """args:
            width: width of the canvas (default 1000)
            height: height of the canvas (default 600)
        """
        self.width = width
        self.height = height

    @property
    def width(self):
        """get width"""
        return self._width

    @width.setter
    def width(self, value):
        """set width"""
        if not isinstance(value, int):
            raise TypeError("width must be an integer")
        if value < 100:
            raise ValueError("width must be greater than 100")
        self._width = value

    @property
    def height(self):
        """get height"""
        return self._height

    @height.setter
    def height(self, value):
        """set height"""
        if not isinstance(value, int):
            raise TypeError("height must be an integer")
        if value < 50:
            raise ValueError("height must be greater than 50")
        self._height = value


class OptionsColor:
    """class used for storing color options"""

    def __init__(self, bodies_r=255, bodies_g=255, bodies_b=255,
                 pointers_r=255, pointers_g=0, pointers_b=0):
        """args:
            bodies_*: RGB value of body color (defaults 255, 255, 255)
            pointers_*: RGB value of pointer color (defaults 255, 0, 0)
        """
        self.bodies = vp.vector(bodies_r, bodies_g, bodies_b)
        self.pointers = vp.vector(pointers_r, pointers_g, pointers_b)

    @property
    def bodies(self):
        """get bodies color vector"""
        return self._bodies

    @bodies.setter
    def bodies(self, value):
        """set bodies color vector"""
        if not (0 <= value.x <= 255 and 0 <= value.y <= 255
                and 0 <= value.z <= 255):
            raise ValueError("RGB values must be between 0 and 255")
        self._bodies = value

    @property
    def pointers(self):
        """get pointers color vector"""
        return self._pointers

    @pointers.setter
    def pointers(self, value):
        """set pointers color vector"""
        if not (0 <= value.x <= 255 and 0 <= value.y <= 255
                and 0 <= value.z <= 255):
            raise ValueError("RGB values must be between 0 and 255")
        self._pointers = value


class Options:
    """class used for option input"""

    def __init__(self, canvas_width=1000, canvas_height=600,
                 color_objects_r=255, color_objects_g=255,
                 color_objects_b=255, color_pointers_r=255,
                 color_pointers_g=0, color_pointers_b=0, show_pointers=1,
                 update_rate=100, max_seconds=30, delta_t=10,
                 central_centered=0, testing=0, restart=1):
        """args:
            canvas_*: dimensions of vpython canvas (defaults 1000, 600)
            color_bodies_*: RGB value of body color (defaults 255, 255, 255)
            color_pointers_*: RGB value of pointer color (defaults 255, 0, 0)
            show_pointers: optional pointers to objects (default 1)
            update_rate: calculations per second (default 100)
            max_seconds: simulation time in s (default 30)
            delta_t: Δt value (seconds in one calculation) (default 10)
            central_centered: center central body during simulation (default 0)
            testing: enable testing features (default 0)
            restart: restart the whole program after one simulation (default 1)
        """
        self.canvas = OptionsCanvas(width=canvas_width, height=canvas_height)
        self.colors = OptionsColor(bodies_r=color_objects_r,
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
        """create Options object from dictionary

        args:
            values: dictionary of options to be used
        """
        return cls(canvas_width=values["canvas"]["width"],
                   canvas_height=values["canvas"]["height"],
                   color_objects_r=values["color"]["objects"]["r"],
                   color_objects_g=values["color"]["objects"]["g"],
                   color_objects_b=values["color"]["objects"]["b"],
                   color_pointers_r=values["color"]["pointers"]["r"],
                   color_pointers_g=values["color"]["pointers"]["g"],
                   color_pointers_b=values["color"]["pointers"]["b"],
                   show_pointers=values["show_pointers"],
                   update_rate=values["update_rate"],
                   max_seconds=values["max_seconds"],
                   delta_t=values["t_factor"],
                   central_centered=values["do_central_centered"],
                   testing=values["do_testing"], restart=values["do_restart"])

    @classmethod
    def from_list(cls, values):
        """create Options object form list or tuple

        args:
            values: list or tuple of options to be used
        """
        return cls(canvas_width=values[0], canvas_height=values[1],
                   color_objects_r=values[2], color_objects_g=values[3],
                   color_objects_b=values[4], color_pointers_r=values[5],
                   color_pointers_g=values[6], color_pointers_b=values[7],
                   show_pointers=values[8], update_rate=values[9],
                   max_seconds=values[10], delta_t=values[11],
                   central_centered=values[12], testing=values[13],
                   restart=values[14])

    @property
    def rate(self):
        """get update rate"""
        return self._rate

    @rate.setter
    def rate(self, value):
        """set update rate"""
        if not isinstance(value, int):
            raise TypeError("rate must be an integer")
        if value < 1:
            raise ValueError("rate must be positive")
        self._rate = value

    @property
    def sim_time(self):
        """get simulation time"""
        return self._sim_time

    @sim_time.setter
    def sim_time(self, value):
        """set simulation time"""
        if not isinstance(value, int):
            raise TypeError("sim_time must be an integer")
        if value < 0:
            raise ValueError("sim_time must be greater than 0 (zero)")
        self._sim_time = value

    @property
    def delta_t(self):
        """get Δt"""
        return self._delta_t

    @delta_t.setter
    def delta_t(self, value):
        """set Δt"""
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError("delta_t must be a number")
        if value <= 0:
            raise ValueError("delta_t must be positive")
        self._delta_t = value

    def to_dict(self) -> dict:
        """converts the Options object to a dictionary

        returns: dict
        """
        return {
            "canvas": {
                "width": self.canvas.width,
                "height": self.canvas.height
            },
            "color": {
                "objects": {
                    "r": self.colors.bodies.x,
                    "g": self.colors.bodies.y,
                    "b": self.colors.bodies.z
                },
                "pointer": {
                    "r": self.colors.pointers.x,
                    "g": self.colors.pointers.y,
                    "b": self.colors.pointers.z
                },
            },
            "show_pointers": self.pointers,
            "update_rate": self.rate,
            "max_seconds": self.sim_time,
            "t_factor": self.delta_t,
            "do_central_centered": self.central_centered,
            "do_testing": self.testing,
            "do_restart": self.restart
        }
