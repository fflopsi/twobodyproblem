import vpython as vp


class Body(vp.sphere):
    """class used for displaying vpython spheres with additional attributes

    inherits from: vpython.sphere
    """

    def __init__(self, sim, name: str, mass=1.0, velocity=vp.vector(0, 0, 0),
                 **kwargs):
        """constructor extends vpython.sphere constructor

        additional args:
            sim: simulation where the bodies are created in
            name: the name of the body
            mass: the mass of the body (default 1.0)
            velocity: the initial velocity of the body (as vpython.vector)
        """
        super(Body, self).__init__(**kwargs)
        self.parent = sim
        self._name = name
        self._mass = mass
        self.velocity = velocity
        self.force = vp.vector(0, 0, 0)
        self.acceleration = vp.vector(0, 0, 0)

    @property
    def name(self):
        """get the name of the body"""
        return self._name

    @property
    def mass(self):
        """get the mass of the body"""
        return self._mass

    @property
    def force(self):
        """get and set the force of the body"""
        return self._force

    @force.setter
    def force(self, value: vp.vector):
        if not isinstance(value, vp.vector):
            raise TypeError("force must be a vector")
        self._force = value

    @property
    def acceleration(self):
        """get and set the acceleration of the body"""
        return self._acceleration

    @acceleration.setter
    def acceleration(self, value: vp.vector):
        if not isinstance(value, vp.vector):
            raise TypeError("acceleration must be a vector")
        self._acceleration = value

    @property
    def velocity(self):
        """get and set the velocity of the body"""
        return self._velocity

    @velocity.setter
    def velocity(self, value: vp.vector):
        if not isinstance(value, vp.vector):
            raise TypeError("velocity must be a vector")
        self._velocity = value

    def calculate(self, delta_t=10):
        """calculate new acceleration, velocity and position from force
        (calculation beforehand needed), mass, previous velocity and position

        args:
            delta_t: Δt value (seconds in one calculation) (default 10)
        """
        self.acceleration = self.force / self.mass
        self.velocity = self.acceleration * delta_t + self.velocity
        self.pos = self.velocity * delta_t + self.pos
