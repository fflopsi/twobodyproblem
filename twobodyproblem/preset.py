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
    mass: float
    radius: float
    mass_unit = "kg"
    radius_unit = "m"


class Sun(AstroBody):
    mass = 1.989e30
    radius = 6.9634e8


class Earth(AstroBody):
    mass = 5.972e24
    radius = 6.371e6


class Moon(AstroBody):
    mass = 7.342e22
    radius = 1.737e6


class Sputnik2(AstroBody):
    mass = 5e2
    radius = 2e0


def distance(one: AstroBody, two: AstroBody) -> float:
    if one.mass > two.mass:
        return DISTANCE[one.__name__][two.__name__]
    else:
        return DISTANCE[two.__name__][one.__name__]
