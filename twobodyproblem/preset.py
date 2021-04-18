import os

import yaml

with open(os.path.dirname(os.path.realpath(__file__))
          + "/saved_data/presets.yml") as f:
    presets = yaml.load(f, Loader=yaml.FullLoader)


class AstroBody:
    """base class of which all preset classes should inherit"""
    values: dict
    mass: float
    radius: float
    mass_unit = "kg"
    radius_unit = "m"


class Sun(AstroBody):
    """class for Sun presets, inherits from AstroBody"""
    values = presets["Sun"]
    mass = values["mass"]
    radius = values["radius"]


class Earth(AstroBody):
    """class for Earth presets, inherits from AstroBody"""
    values = presets["Earth"]
    mass = values["mass"]
    radius = values["radius"]


class Moon(AstroBody):
    """class for Moon presets, inherits from AstroBody"""
    values = presets["Moon"]
    mass = values["mass"]
    radius = values["radius"]


class Sputnik2(AstroBody):
    """class for Sputnik 2 presets, inherits from AstroBody"""
    values = presets["Sputnik2"]
    mass = values["mass"]
    radius = values["radius"]


def mass(body: str) -> float:
    """returns mass of given body

    args:
        body: string which body's mass should be returned

    returns: float
    """
    if isinstance(body, str):
        return presets[body]["mass"]
    else:
        raise TypeError("body must be of type str")


def radius(body: str) -> float:
    """returns radius of given body

    args:
        body: string which body's radius should be returned

    returns: float
    """
    if isinstance(body, str):
        return presets[body]["radius"]
    else:
        raise TypeError("body must be of type str")


def distance(name: str) -> float:
    """returns distance between two given bodies

    args:
        name: name of distance that should be returned

    returns: float
    """
    if isinstance(name, str):
        return presets["distance"][name]
    else:
        raise TypeError("name must be of type str")
