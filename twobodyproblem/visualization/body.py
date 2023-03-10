import vpython as vp


class Body(vp.sphere):
    """Displays vpython spheres with additional attributes

    Inherits from: vpython.sphere

    Attributes:
    parent: The simulation to where the Body belongs
    name: The name of the Body
    mass: The mass of the Body
    velocity: The current velocity of the Body as vpython vector in x, y, z
    force: The current force upon the Body as vpython vector in x, y, z
    acceleration: The current acceleration of the Body as vpython vector in x, y, z
    """

    def __init__(self, sim, name: str, mass=1.0, velocity=vp.vector(0, 0, 0),
                 **kwargs):
        """Constructor extends vpython.sphere constructor"""
        super(Body, self).__init__(**kwargs)
        self.parent = sim
        self._name = name
        self._mass = mass
        self.velocity = velocity
        self.force = vp.vector(0, 0, 0)
        self.acceleration = vp.vector(0, 0, 0)

    @property
    def name(self):
        """Get the name of the body"""
        return self._name

    @property
    def mass(self):
        """Get the mass of the body"""
        return self._mass

    @property
    def force(self):
        """Get and set the force of the body"""
        return self._force

    @force.setter
    def force(self, value: vp.vector):
        if not isinstance(value, vp.vector):
            raise TypeError("force must be a vector")
        self._force = value

    @property
    def acceleration(self):
        """Get and set the acceleration of the body"""
        return self._acceleration

    @acceleration.setter
    def acceleration(self, value: vp.vector):
        if not isinstance(value, vp.vector):
            raise TypeError("acceleration must be a vector")
        self._acceleration = value

    @property
    def velocity(self):
        """Get and set the velocity of the body"""
        return self._velocity

    @velocity.setter
    def velocity(self, value: vp.vector):
        if not isinstance(value, vp.vector):
            raise TypeError("velocity must be a vector")
        self._velocity = value

    def calculate(self, delta_t=10):
        """Calculate new acceleration, velocity and position from force
        (calculation beforehand needed), mass, previous velocity and position

        Arguments:
        delta_t: Δt value (seconds in one calculation) (default 10)
        """
        self.acceleration = self.force / self.mass
        self.velocity = self.acceleration * delta_t + self.velocity
        self.pos = self.velocity * delta_t + self.pos
