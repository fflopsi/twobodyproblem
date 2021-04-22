import os
from pathlib import Path

import vpython as vp
import yaml


class ValuesBody:
    """class used for representing bodies in Values"""

    def __init__(self, mass, radius, v0_x=0.0, v0_y=0.0, v0_z=0.0):
        """args:
            mass: the mass of the body
            radius: the radius of the body
            v0_*: the starting velocity of the body (defaults 0, 0, 0)
        """
        self.mass = mass
        self.radius = radius
        self.velocity = vp.vector(v0_x, v0_y, v0_z)

    @property
    def mass(self):
        """get and set mass"""
        return self._mass

    @mass.setter
    def mass(self, value):
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError("mass must be a number")
        if value == 0:
            raise ValueError("mass must not be 0 (zero)")
        self._mass = value

    @property
    def radius(self):
        """get and set radius"""
        return self._radius

    @radius.setter
    def radius(self, value):
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError("radius must be a number")
        if value <= 0:
            raise ValueError("radius must be positive")
        self._radius = value

    @property
    def velocity(self):
        """get and set velocity"""
        return self._velocity

    @velocity.setter
    def velocity(self, value: vp.vector):
        if not isinstance(value, vp.vector):
            raise TypeError("velocity must be a vector")
        self._velocity = value


class Values:
    """class used for value input"""

    directory = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, central_mass=5.972e+24, central_radius=6371000.0,
                 central_v0_x=0.0, central_v0_y=0.0, central_v0_z=0.0,
                 sat_mass=500.0, sat_radius=2.0, sat_v0_x=0.0, sat_v0_y=0.0,
                 sat_v0_z=-8000.0, distance=1000000.0):
        """args:
            central_mass: mass of first body (default 5.972e+24)
            central_radius: radius of first body (default 6371000)
            central_v0_*: starting velocity of first body (defaults 0, 0, 0)
            sat_mass: mass of second body (default 500)
            sat_radius: radius of second body (default 2)
            sat_v0_*: starting velocity of second body (defaults 0, 0, 0)
            distance: starting distance between bodies (default 1000000)
        """
        self.central = ValuesBody(mass=central_mass, radius=central_radius,
                                  v0_x=central_v0_x, v0_y=central_v0_y,
                                  v0_z=central_v0_z)
        self.sat = ValuesBody(mass=sat_mass, radius=sat_radius,
                              v0_x=sat_v0_x, v0_y=sat_v0_y, v0_z=sat_v0_z)
        self.distance = distance

    @classmethod
    def from_dict(cls, values: dict):
        """create Values object from dictionary

        args:
            values: dictionary of values to be used

        returns: Values
        """
        return cls(central_mass=values["central_mass"],
                   central_radius=values["central_radius"],
                   central_v0_x=values["central_v0"]["x"],
                   central_v0_y=values["central_v0"]["y"],
                   central_v0_z=values["central_v0"]["z"],
                   sat_mass=values["sat_mass"],
                   sat_radius=values["sat_radius"],
                   sat_v0_x=values["sat_v0"]["x"],
                   sat_v0_y=values["sat_v0"]["y"],
                   sat_v0_z=values["sat_v0"]["z"],
                   distance=values["distance"])

    @classmethod
    def from_list(cls, values):
        """create Values object from list or tuple

        args:
            values: list or tuple to be used

        returns: Values
        """
        return cls(central_mass=values[0], central_radius=values[1],
                   central_v0_x=values[2], central_v0_y=values[3],
                   central_v0_z=values[4], sat_mass=values[5],
                   sat_radius=values[6], sat_v0_x=values[7],
                   sat_v0_y=values[8], sat_v0_z=values[9], distance=values[10])

    @classmethod
    def from_file(cls, path=None):
        """create Values object from yaml file

        args:
            path: path to file (default [user home dir]/Documents/
                TwoBodyProblem/default/values.yml)

        returns: Values
        """
        dir_path = str(Path.home()) + "/Documents/TwoBodyProblem/default"
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        if path is None:
            path = dir_path + "/values.yml"
        with open(path, "r") as f:
            return cls.from_dict(yaml.load(f, Loader=yaml.FullLoader))

    @property
    def distance(self):
        """get and set distance between bodies"""
        return self._distance

    @distance.setter
    def distance(self, value):
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError("distance must be a number")
        self._distance = value

    def to_dict(self) -> dict:
        """converts the Values object to a dictionary

        returns: dict
        """
        return {
            "central_mass": self.central.mass,
            "central_radius": self.central.radius,
            "central_v0": {
                "x": self.central.velocity.x,
                "y": self.central.velocity.y,
                "z": self.central.velocity.z
            },
            "sat_mass": self.sat.mass,
            "sat_radius": self.sat.radius,
            "sat_v0": {
                "x": self.sat.velocity.x,
                "y": self.sat.velocity.y,
                "z": self.sat.velocity.z
            },
            "distance": self.distance
        }

    def save(self, path=None):
        """save content of self to yaml file (overwriting existing content)

        args:
            path: path to file (default [user home dir]/Documents/
                TwoBodyProblem/default/values.yml)
        """
        dir_path = str(Path.home()) + "/Documents/TwoBodyProblem/default"
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        if path is None:
            path = dir_path + "/values.yml"
        with open(path, "w+") as f:
            f.write(yaml.dump(self.to_dict()))
