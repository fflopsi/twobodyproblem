import os

import yaml

with open(os.path.dirname(os.path.realpath(__file__)) + "/saved_data/presets.yml") as f:
    presets = yaml.load(f, Loader=yaml.FullLoader)

MASS = {
    "UNIT": "kg",
    "Sun": 1.989e30,
    "Earth": 5.972e24,
    "Moon": 7.342e22,
    "Sputnik2": 5.0e2
}

RADIUS = {
    "UNIT": "m",
    "Sun": 6.9634e8,
    "Earth": 6.371e6,
    "Moon": 1.737e6,
    "Sputnik2": 2.0e0
}

DISTANCE = {
    "UNIT": "m",
    "Sun": {
        "Sun": 1.496e11,
        "Earth": 1.496e11,
        "Moon": 1.496e11,
        "Sputnik2": 1.496e24
    },
    "Earth": {
        "Earth": 3.844e8,
        "Moon": 3.844e8,
        "Sputnik2": 1e6
    },
    "Moon": {
        "Moon": 3.844e8,
        "Sputnik2": 1e6
    }
}


class AstroBody:
    """base class of which all preset classes should inherit"""
    mass: float
    radius: float
    mass_unit = "kg"
    radius_unit = "m"


class Sun(AstroBody):
    """class for Sun presets, inherits from AstroBody"""
    mass = MASS["Sun"]
    radius = RADIUS["Sun"]


class Earth(AstroBody):
    """class for Earth presets, inherits from AstroBody"""
    mass = MASS["Earth"]
    radius = RADIUS["Earth"]


class Moon(AstroBody):
    """class for Moon presets, inherits from AstroBody"""
    mass = MASS["Moon"]
    radius = RADIUS["Moon"]


class Sputnik2(AstroBody):
    """class for Sputnik 2 presets, inherits from AstroBody"""
    mass = MASS["Sputnik2"]
    radius = RADIUS["Sputnik2"]


def mass(body: AstroBody) -> float:
    """returns mass of given body

    args:
        body: AstroBody of which mass should be given

    returns: float
    """
    return body.mass


def radius(body: AstroBody) -> float:
    """returns radius of given body

    args:
        body: AstroBody of which radius should be given

    returns: float
    """
    return body.radius


def distance(one: AstroBody, two: AstroBody) -> float:
    """returns distance between two given bodies

    args:
        one: first AstroBody
        two: second AstroBody

    returns: float
    """
    if one.mass > two.mass:
        return DISTANCE[one.__name__][two.__name__]
    else:
        return DISTANCE[two.__name__][one.__name__]
