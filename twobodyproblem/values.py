import os
from pathlib import Path

import vpython as vp
import yaml

defaults = (5.972e+24, 6371000.0, 0.0, 0.0, 0.0, 500.0, 2.0, 0.0, 0.0, -8000.0, 1000000.0)


class Values:
    """Contains all values used in the simulation
    
    Attributes:
    central: The central Body, usually the more massive one
    sat: The second Body (satellite)
    distance: Starting distance between the two bodies
    """

    class Body:
        """Represents bodies
        
        Attributes:
        mass: The mass of the body in kg
        radius: The radius of the body in m
        velocity: The velocity of the body in m/s in x, y, z directions
        """

        def __init__(self, mass, radius, v0_x=0.0, v0_y=0.0, v0_z=0.0):
            """Initialize a Body with an initial velocity v0 in x, y, z"""
            self.mass = mass
            self.radius = radius
            self.velocity = vp.vector(v0_x, v0_y, v0_z)

        @property
        def mass(self):
            """Get and set mass"""
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
            """Get and set radius"""
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
            """Get and set velocity"""
            return self._velocity

        @velocity.setter
        def velocity(self, value: vp.vector):
            if not isinstance(value, vp.vector):
                raise TypeError("velocity must be a vector")
            self._velocity = value

    def __init__(self, central_mass=defaults[0], central_radius=defaults[1],
                 central_v0_x=defaults[2], central_v0_y=defaults[3], central_v0_z=defaults[4],
                 sat_mass=defaults[5], sat_radius=defaults[6], sat_v0_x=defaults[7],
                 sat_v0_y=defaults[8], sat_v0_z=defaults[9], distance=defaults[10]):
        """Initialize a Values object with the details for central and sat bodies"""
        self.central = self.Body(mass=central_mass, radius=central_radius, v0_x=central_v0_x,
                                 v0_y=central_v0_y, v0_z=central_v0_z)
        self.sat = self.Body(mass=sat_mass, radius=sat_radius, v0_x=sat_v0_x, v0_y=sat_v0_y,
                             v0_z=sat_v0_z)
        self.distance = distance

    @classmethod
    def from_dict(cls, values: dict):
        """Create Values object from dictionary"""
        return cls(central_mass=values["central_mass"], central_radius=values["central_radius"],
                   central_v0_x=values["central_v0"]["x"], central_v0_y=values["central_v0"]["y"],
                   central_v0_z=values["central_v0"]["z"], sat_mass=values["sat_mass"],
                   sat_radius=values["sat_radius"], sat_v0_x=values["sat_v0"]["x"],
                   sat_v0_y=values["sat_v0"]["y"], sat_v0_z=values["sat_v0"]["z"],
                   distance=values["distance"])

    @classmethod
    def from_list(cls, values):
        """Create Values object from list or tuple"""
        return cls(central_mass=values[0], central_radius=values[1], central_v0_x=values[2],
                   central_v0_y=values[3], central_v0_z=values[4], sat_mass=values[5],
                   sat_radius=values[6], sat_v0_x=values[7], sat_v0_y=values[8], sat_v0_z=values[9],
                   distance=values[10])

    @classmethod
    def from_file(cls, path=None):
        """Create Values object from yaml file

        Arguments:
        path: path to file (default [user home dir]/Documents/
            TwoBodyProblem/default/values.yml)
        """
        dir_path = str(Path.home()) + "/Documents/TwoBodyProblem/default"
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        if path is None:
            path = dir_path + "/values.yml"
        with open(path, "r") as f:
            return cls.from_dict(yaml.load(f, Loader=yaml.FullLoader))

    @classmethod
    def from_input(cls):
        """Create Values object from user input"""
        values = list(defaults)
        print("Central body:")
        try:
            values[0] = float(input("\tMass (5.972e+24)[kg]: "))
        except ValueError:
            pass
        try:
            values[1] = float(input("\tRadius (6371000)[m]: "))
        except ValueError:
            pass
        print("\tStarting velocity [m/s]:")
        try:
            values[2] = float(input("\t\tSpeed in x (0): "))
        except ValueError:
            pass
        try:
            values[3] = float(input("\t\tSpeed in y (0): "))
        except ValueError:
            pass
        try:
            values[4] = float(input("\t\tSpeed in z (0): "))
        except ValueError:
            pass
        print("Satellite / second body:")
        try:
            values[5] = float(input("\tMass (500)[kg]: "))
        except ValueError:
            pass
        try:
            values[6] = float(input("\tRadius (2)[m]: "))
        except ValueError:
            pass
        print("\tStarting velocity [m/s]:")
        try:
            values[7] = float(input("\t\tSpeed in x (0): "))
        except ValueError:
            pass
        try:
            values[8] = float(input("\t\tSpeed in y (0): "))
        except ValueError:
            pass
        try:
            values[9] = float(input("\t\tSpeed in z (-8000): "))
        except ValueError:
            pass
        try:
            values[10] = float(input("\tInitial distance (1000000)[m]: "))
        except ValueError:
            pass

        return cls.from_list(values)

    @property
    def distance(self):
        """Get and set distance between bodies"""
        return self._distance

    @distance.setter
    def distance(self, value):
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError("distance must be a number")
        self._distance = value

    def to_dict(self) -> dict:
        """Converts the Values object to a dictionary"""
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
        """Save content of self to yaml file (overwriting existing content)

        Arguments:
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
